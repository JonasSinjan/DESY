! NB NB NB NB NB
! Note on how FFTW stores the $k$ values in the arrays
!  first dimension: 0, 1, 2, ... n/2  (take integer division into account on last term)
!  second dimension - n even: 0, 1, 2, ... n/2, -n/2 + 1, - n/2 + 2, ... -1
!  second dimension - n odd:  0, 1, 2, ... n/2, -n/2, n/2 + 1, ... -1

program main

  !use spectrum, only: power_kk, dft_filter
  use, intrinsic :: iso_c_binding
  use omp_lib
  implicit none

  ! ------------------------------------------------------------------------
  ! include FFTW
  ! ------------------------------------------------------------------------
  !include 'fftw3.f03'

  integer :: start_time, stop_time !timing fortran program
  integer :: count_rate, count_max

  ! ------------------------------------------------------------------------
  ! define fixed parameters
  ! ------------------------------------------------------------------------
#ifdef DP
  integer, parameter :: sp = kind(1.d0)
#else
  integer, parameter :: sp = kind(1.0)
#endif
  !double preicision, real number (with decimal) not integer
  integer, parameter :: dp = kind(1.d0)

  real(dp), parameter :: pi = acos(-1.d0)
  real(dp), parameter :: twopi = 2.d0*pi
  real(dp), allocatable :: wtime, tot_time
  real(dp), allocatable :: time_init, time_final, elapsed_time
  integer, allocatable :: threadno
  integer :: thread_id

  ! ------------------------------------------------------------------------
  ! define and initialize problem parameters
  ! ------------------------------------------------------------------------
  integer :: ngrids = 10
  real(sp) :: anis = 1.
  real(sp) :: lx = twopi ! this the box space in fourier space?
  real(sp) :: ly = twopi
  real(sp) :: lz = twopi
  real(sp) :: bx0 = 1.
  real(sp) :: by0 = 0.
  real(sp) :: bz0 = 0. !3d

  ! ------------------------------------------------------------------------
  ! define variables
  ! ------------------------------------------------------------------------
  integer :: n, num_seed
  integer, dimension(1) :: rand_seed
  integer, allocatable :: seed(:)
  real(sp) :: num
  real(sp) :: h
  real(sp) :: amp
  real(sp) :: kx, ky, kz

  real(sp), dimension(:), allocatable :: x, y, z
  real(sp), dimension(:,:,:), allocatable :: bx, by, bz !3d
  real(sp) :: time, dx, dy, dz

  integer :: nk, nkb, nkt

  logical :: lsum_power

  ! ------------------------------------------------------------------------
  ! define auxiliary variables
  ! ------------------------------------------------------------------------
  type(C_PTR) :: plan_phi0
  type(C_PTR) :: plan1, plan2
  type(C_PTR) :: plan
  integer*8 :: dftplan
  real(sp), dimension(:,:,:), allocatable :: f

  real(sp) :: kmax, kmod, mag
  real(sp) :: test_var
  real(sp) :: k_para, k_perp, E_coeff, ph


  ! ------------------------------------------------------------------------
  ! define dummy variables
  ! ------------------------------------------------------------------------
  integer :: l,q
  integer :: m
  integer :: i, j, k
  integer :: ii, jj, k_k
  integer :: ki, kj, kk !3d
  integer :: lun

  character(len=400) :: data_dir
  character(len=1024) :: file_out
  character(len=400) :: cmd
  
  time = 0.

  wtime = omp_get_wtime()
  ! ------------------------------------------------------------------------
  ! specify folder for output data
  ! ------------------------------------------------------------------------
  data_dir = './Runs/512_1st_B/'

  cmd = 'mkdir -p ' // trim(data_dir)
  call system(cmd)

  ! ------------------------------------------------------------------------
  ! calculate grid parameters
  ! ------------------------------------------------------------------------
  n = 2**(ngrids) + 1

  call random_seed(size = num_seed)
  allocate(seed(num_seed))

  ! creating random seed
  do i = 1, num_seed
    seed(i) = i*4251
  enddo

  call random_seed(put=seed)

! ------------------------------------------------------------------------
  ! allocate arrays
  ! ------------------------------------------------------------------------

  allocate(x(n))
  allocate(y(n))
  allocate(z(n))!3d

  ! ------------------------------------------------------------------------
  ! set space grid and time of output files
  ! ------------------------------------------------------------------------
  dx = lx/real(n)
  dy = ly/real(n)
  dz = lz/real(n) !3d

  do i = 1, n
    x(i) = (real(i) - 0.5)*dx
  enddo

  do j = 1, n
    y(j) = (real(j) - 0.5)*dy
  enddo

  do k = 1, n !3d n instead of 1,1
    z(k) = (real(k) - 0.5)*dz
  enddo


  ! ------------------------------------------------------------------------
  ! build bx, by and bz and write to file
  ! ------------------------------------------------------------------------
  allocate (bx(n,n,n)) !n,n,n for all?
  allocate (by(n,n,n))
  allocate (bz(n,n,n)) !3d

  !-------------------------------------------------------------------
  !3 arrays allocated
  !-------------------------------------------------------------------

  bx(:,:,:) = bx0 ! :,:,:? for 3d
  by(:,:,:) = by0
  bz(:,:,:) = bz0 !3d

  !do I need to vary in 3rd direction now too? k?
  do k = 1, n
    do j = 1, n
      do i = 1, n
        by(i,j,k) = by(i,j,k) + 0.5*sin(2.0*x(i))
        by(i,j,k) = by(i,j,k) + 0.5*sin(4.0*x(i)+1.6)
        
        ! 2nd B perturb
        ! by(i,j,k) = by(i,j,k) + 2.5*sin(2.0*x(i))
        ! by(i,j,k) = by(i,j,k) + 1.5*sin(4.0*x(i)+1.6)
        ! bx(i,j,k) = bx(i,j,k) + 5*cos(2.0*y(j))
        ! bx(i,j,k) = bx(i,j,k) + 3*cos(4.0*y(j)+1.6)
      enddo
    enddo
  enddo

  lun = 701
  file_out = trim(data_dir) // '/' // 'BX.BIN'
  ! bx(:,:,:)?
  open(unit=lun, file=trim(file_out), form='unformatted', status='replace', action='write', access='stream')
    write(lun) bx(:,:,:)
  close(lun)

  lun = 701
  file_out = trim(data_dir) // '/' // 'BY.BIN'
  ! by(:,:,:)?
  open(unit=lun, file=trim(file_out), form='unformatted', status='replace', action='write', access='stream')
    write(lun) by(:,:,:)
  close(lun)

  !3d
  lun = 701
  file_out = trim(data_dir) // '/' // 'BZ.BIN'
  ! bz(:,:,:)?
  open(unit=lun, file=trim(file_out), form='unformatted', status='replace', action='write', access='stream')
    write(lun) bz(:,:,:)
  close(lun)
 
  wtime = omp_get_wtime() - wtime

  print *, "Time taken = ", wtime

end program main