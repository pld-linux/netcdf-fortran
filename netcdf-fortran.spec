#
# Conditional build:
%bcond_without	f90		# don't build Fortran 90 interface (just builtin F77)
%bcond_without	tests		# don't perform "make check"
				# (note: tests need endoder-enabled szip)
#
Summary:	NetCDF Fortran library
Summary(pl.UTF-8):	Biblioteka NetCDF dla języka Fortran
Name:		netcdf-fortran
Version:	4.2
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/%{name}-%{version}.tar.gz
# Source0-md5:	cc3bf530223e8f4aff93793b9f197bf3
Patch0:		%{name}-f90.patch
Patch1:		%{name}-info.patch
URL:		http://www.unidata.ucar.edu/packages/netcdf/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%if %{with f90}
BuildRequires:	gcc-fortran >= 5:4.0
%else
BuildRequires:	gcc-g77
%endif
BuildRequires:	libtool >= 2:2.2
BuildRequires:	netcdf-devel >= 4.2
BuildRequires:	texinfo
Requires:	netcdf >= 4.2
Obsoletes:	netcdf-f90
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
%if %{with f90}
Requires:	gcc-fortran >= 5:4.0
%else
Requires:	gcc-g77
%endif
Requires:	netcdf-devel >= 4.2
Obsoletes:	netcdf-f90-devel

%description devel
Header files for netCDF - Fortran interface.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki netCDF - interfejs dla języka Fortran.

%package static
Summary:	NetCDF Fortran static library
Summary(pl.UTF-8):	Biblioteka statyczna netCDF dla języka Fortran
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	netcdf-f90-static

%description static
Static version of netCDF Fortran library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki netCDF dla języka Fortran.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# specify gFortran, configure detection may fail if FC specifies *-gfortran different `which gfortran`
CPPFLAGS="%{rpmcppflags} -DgFortran=1"
%configure \
	FCFLAGS="%{rpmcflags}" \
	%{!?with_f90:--disable-f90}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%doc COPYRIGHT README
%attr(755,root,root) %{_libdir}/libnetcdff.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetcdff.so.5

%files devel
%defattr(644,root,root,755)
%doc man4/netcdf-f77.html man4/netcdf-f90.html
%attr(755,root,root) %{_bindir}/nf-config
%attr(755,root,root) %{_libdir}/libnetcdff.so
%{_libdir}/libnetcdff.la
%{_includedir}/netcdf.inc
%{_pkgconfigdir}/netcdf-fortran.pc
%{_mandir}/man3/netcdf_f77.3*
%{_infodir}/netcdf-f77.info*
%if %{with f90}
%{_includedir}/netcdf.mod
%{_includedir}/typesizes.mod
%{_mandir}/man3/netcdf_f90.3*
%{_infodir}/netcdf-f90.info*
%endif

%files static
%defattr(644,root,root,755)
%{_libdir}/libnetcdff.a
