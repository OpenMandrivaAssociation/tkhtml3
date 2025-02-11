%define cvs		20081201
%define polipo_version	1.0.4

Summary:	Tk HTML / CSS rendering widget
Name:		tkhtml3
Version:	3.0
Release:	%mkrel 0.%{cvs}.7
License:	BSD
Group:		System/Libraries
URL:		https://tkhtml.tcl.tk/
# CVS instructions on site
Source0:	http://tkhtml.tcl.tk/%{name}-%{cvs}.tar.lzma
# Disable a whole optional block of code which seems to cause errors
# - AdamW 2008/12
# hv3 expects a patched (see hv3_polipo.patch) polipo, named
# hv3_polipo, to be available in $PATH. Without it, some things -
# notably ssl support - don't seem to work. - AdamW 2008/12
Source1:	http://www.pps.jussieu.fr/~jch/software/files/polipo/polipo-%{polipo_version}.tar.gz
Patch0:		tkhtml3-20081201-statesock.patch
# Patch for Polipo (see above) - AdamW 2008/12
Patch1:		hv3_polipo.patch
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	libx11-devel
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
BuildRequires:	libgc-devel
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
%setup -q -n htmlwidget -b 1
%patch0 -p1 -b .statesock
pushd %{_builddir}/polipo-%{polipo_version}
%patch1 -p1 -b .hv3_polipo
popd

%build
mkdir build
pushd build
CONFIGURE_TOP=.. %{configure2_5x} --libdir=%{tcl_sitearch}
%make
# Build tclsee
make -f ../linux-gcc.mk tclsee TOP=.. JSLIB="%{_libdir}/libgc.so %{_libdir}/libsee.so" JSFLAGS="$JSFLAGS %{optflags} -fPIC"
popd
# Build Polipo
pushd %{_builddir}/polipo-%{polipo_version}
%make
popd

%install
rm -fr %buildroot
pushd build
%makeinstall_std
cp -R tclsee0.1 %{buildroot}%{tcl_sitearch}
popd

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-hv3.desktop <<EOF
[Desktop Entry]
Name=Hv3
Comment=Very light web browser
Exec=%{_bindir}/hv3
Icon=web_browser_section
Terminal=false
Type=Application
StartupNotify=true
MimeType=foo/bar;foo2/bar2;
Categories=Network;WebBrowser;
EOF


mkdir -p %{buildroot}%{tcl_sitelib}/hv3
cp hv/*.tcl %{buildroot}%{tcl_sitelib}/hv3/
rm %{buildroot}%{tcl_sitelib}/hv3/tst_main.tcl
rm %{buildroot}%{tcl_sitelib}/hv3/main.tcl
echo '#!/bin/sh' > %{buildroot}%{_bindir}/hv3
echo 'exec wish %{tcl_sitelib}/hv3/hv3_main.tcl "$@"' >> %{buildroot}%{_bindir}/hv3
chmod 755 %{buildroot}%{_bindir}/hv3

install -m 0755 %{_builddir}/polipo-%{polipo_version}/polipo %{buildroot}%{_bindir}/hv3_polipo

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
%{_bindir}/hv3_polipo
%{_datadir}/applications/mandriva-hv3.desktop



%changelog
* Tue Feb 01 2011 Funda Wang <fwang@mandriva.org> 3.0-0.20081201.7mdv2011.0
+ Revision: 634771
- tighten BR

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 3.0-0.20081201.6mdv2010.0
+ Revision: 445487
- rebuild

* Tue Dec 09 2008 Adam Williamson <awilliamson@mandriva.org> 3.0-0.20081201.5mdv2009.1
+ Revision: 312333
- just do make, not make all, to build polipo (we don't need the docs)
- add source for polipo and the patch to turn it into hv3_polipo, build and
  install hv3_polipo (required for various hv3 functions to work)

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 3.0-0.20081201.4mdv2009.1
+ Revision: 310529
- add a menu entry

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 3.0-0.20081201.3mdv2009.1
+ Revision: 310471
- OK, this is REALLY the right way to handle the fpic stuff...grumble
- ok, i think this is the proper way to get fPIC in here...
- need fPIC in ldflags too
- build with -fPIC to fix x86-64 build
- import tkhtml3


