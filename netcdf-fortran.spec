#
# Conditional build:
%bcond_without	f2003		# Fortran 2003 interface (beside F77/F90)
%bcond_without	static_libs	# static library
%bcond_without	tests		# unit tests (require encoder-enabled szip)
#
Summary:	NetCDF Fortran library
Summary(pl.UTF-8):	Biblioteka NetCDF dla języka Fortran
Name:		netcdf-fortran
Version:	4.6.1
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	https://downloads.unidata.ucar.edu/netcdf-fortran/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a34fa637abc362776b5165c6e5da324d
Patch0:		%{name}-f90.patch
URL:		https://www.unidata.ucar.edu/software/netcdf/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.13
%if %{with f2003}
BuildRequires:	gcc-fortran >= 6:4.4
%else
BuildRequires:	gcc-fortran >= 5:4.0
%endif
BuildRequires:	libtool >= 2:2.2
BuildRequires:	netcdf-devel >= 4.9.0
BuildRequires:	texinfo
Requires:	netcdf >= 4.9.0
Obsoletes:	netcdf-f90 < 3.6.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NetCDF (network Common Data Form) is an interface for array-oriented
data access and a library that provides an implementation of the
interface. The netCDF library also defines a machine-independent
format for representing scientific data. Together, the interface,
library, and format support the creation, access, and sharing of
scientific data. The netCDF software was developed at the Unidata
Program Center in Boulder, Colorado.

This package contains Fortran 77%{?with_f90: and 90} library.

%description -l pl.UTF-8
NetCDF (Network Common Data Form) jest interfejsem dostępu do danych
zorganizowanych w tablice. Biblioteka netCDF definiuje niezależny od
maszyny format reprezentowania danych naukowych. Interfejs oraz
biblioteka pozwalają na tworzenie, dostęp i współdzielenie danych.
NetCDF powstał w Unidata Program Center w Boulder, Colorado.

Ten pakiet zawiera bibliotekę dla języka Fortran 77%{?with_f90: i 90}.

%package devel
Summary:	Header files for netCDF Fortran interface
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu netCDF dla języka Fortran
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%if %{with f2003}
Requires:	gcc-fortran >= 6:4.4
%else
Requires:	gcc-fortran >= 5:4.0
%endif
Requires:	netcdf-devel >= 4.9.0
Obsoletes:	netcdf-f90-devel < 3.6.2

%description devel
Header files for netCDF - Fortran interface.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki netCDF - interfejs dla języka Fortran.

%package static
Summary:	NetCDF Fortran static library
Summary(pl.UTF-8):	Biblioteka statyczna netCDF dla języka Fortran
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	netcdf-f90-static < 3.6.2

%description static
Static version of netCDF Fortran library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki netCDF dla języka Fortran.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
CPPFLAGS="%{rpmcppflags} -DgFortran=1"
%configure \
	FCFLAGS="%{rpmcflags}" \
	%{!?with_f2003:--disable-f03} \
	%{!?with_static_libs:--disable-static}

%{__make}

%if %{with tests}
%{__make} -j1 check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnetcdff.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README.md RELEASE_NOTES.md
%attr(755,root,root) %{_libdir}/libnetcdff.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdff.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nf-config
%attr(755,root,root) %{_libdir}/libnetcdff.so
%{_libdir}/libnetcdff.settings
%{_includedir}/netcdf.inc
%{_includedir}/netcdf*.mod
%{_includedir}/typesizes.mod
%{_pkgconfigdir}/netcdf-fortran.pc
%{_mandir}/man3/netcdf_f77.3*
%{_mandir}/man3/netcdf_fortran.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnetcdff.a
%endif
