%define cvs	20081201

Summary:	Tk HTML / CSS rendering widget
Name:		tkhtml3
Version:	3.0
Release:	%mkrel 0.%{cvs}.1
License:	BSD
Group:		System/Libraries
URL:		http://tkhtml.tcl.tk/
# CVS instructions on site
Source0:	http://tkhtml.tcl.tk/%{name}-%{cvs}.tar.lzma
# Disable a whole optional block of code which seems to cause errors
# - AdamW 2008/12
Patch0:		tkhtml3-20081201-statesock.patch
# Use -fPIC when building tclsee (needed on x86-64) - AdamW 2008/12
Patch1:		tkhtml3-20081201-fpic.patch
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	X11-devel
Requires:	tcl
Requires:	tk
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
Tkhtml3 is a Tk widget that displays content formatted according to the
HTML and CSS standards. Tkhtml3 is not an end-user application, it is
for Tcl programmers who wish to embed a standards-compliant HTML/CSS
implementation in their applications. 

%package -n tclsee
Summary:	Tcl interface to the libsee Javascript engine
Group:		System/Libraries
Version:	0.1
BuildRequires:	see-devel
BuildRequires:	libgc-static-devel
Requires:	tcl

%description -n tclsee
tclsee is a Tcl interface to the libsee Javascript rendering engine.

%package -n hv3
Summary:	Lightweight Tcl/Tk-based web browser
Group:		Networking/WWW
Version:	3.0
Requires:	tcl
Requires:	tk
Requires:	tkhtml3
Requires:	tclsee
Requires:	tcltls
Requires:	tcl-sqlite3
Requires:	tkimg

%description -n hv3
Hv3 is a lightweight web browser with support for modern web standards
like HTML, CSS, HTTP and ECMAScript (a.k.a. javascript). It is based on
the Tkhtml3 HTML rendering widget and the tclsee Javascript rendering
widget.

%prep
%setup -q -n htmlwidget
%patch0 -p1 -b .statesock
%patch1 -p1 -b .fpic

%build
mkdir build
pushd build
export CFLAGS="$CFLAGS -fPIC"
CONFIGURE_TOP=.. %{configure2_5x} --libdir=%{tcl_sitearch}
%make
# Build tclsee
make -f ../linux-gcc.mk tclsee TOP=../ JSLIB="%{_libdir}/libgc.a %{_libdir}/libsee.a"
popd

%install
pushd build
%makeinstall_std
cp -R tclsee0.1 %{buildroot}%{tcl_sitearch}
popd

mkdir -p %{buildroot}%{tcl_sitelib}/hv3
cp hv/*.tcl %{buildroot}%{tcl_sitelib}/hv3/
rm %{buildroot}%{tcl_sitelib}/hv3/tst_main.tcl
rm %{buildroot}%{tcl_sitelib}/hv3/main.tcl
echo '#!/bin/sh' > %{buildroot}%{_bindir}/hv3
echo 'exec wish %{tcl_sitelib}/hv3/hv3_main.tcl "$@"' >> %{buildroot}%{_bindir}/hv3
chmod 755 %{buildroot}%{_bindir}/hv3

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog COPYRIGHT README
%{tcl_sitearch}/Tkhtml3.0
%{_mandir}/mann/*

%files -n tclsee
%{tcl_sitearch}/tclsee0.1

%files -n hv3
%{tcl_sitelib}/hv3
%{_bindir}/hv3

