# TODO: handle GMP plugins better in browser-plugins architecture (only firefox33+ based browsers supported)
#
# Conditional build:
%bcond_with	gmp_api		# Firefox (GeckoMediaPlugins based) plugin
#
%ifarch x32
%undefine with_gmp_api
%endif
Summary:	H.264 codec library
Summary(pl.UTF-8):	Biblioteka kodeka H.264
Name:		openh264
Version:	2.1.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/cisco/openh264/releases/
Source0:	https://github.com/cisco/openh264/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	52345fac1554251459cd7cc2f8344d7b
Patch0:		%{name}-libdir.patch
Patch1:		no-forced-arch.patch
Patch2:		x32-asm.patch
URL:		http://www.openh264.org/
%{?with_gmp_api:BuildRequires:	gmp-api}
BuildRequires:	libstdc++-devel
%ifarch %{ix86} %{x8664}
BuildRequires:	nasm
%endif
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gmp_plugindir	%{_browserpluginsdir}

%description
OpenH264 is a codec library which supports H.264 encoding and
decoding. It is suitable for use in real time applications such as
WebRTC.

%description -l pl.UTF-8
OpenH264 to biblioteka kodeka obsługująca kodowanie i dekodowanie
H.264. Nadaje się do użycia w aplikacjach czasu rzeczywistego, takich
jak WebRTC.

%package devel
Summary:	Header files for OpenH264 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenH264
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for OpenH264 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenH264.

%package static
Summary:	Static OpenH264 library
Summary(pl.UTF-8):	Statyczna biblioteka OpenH264
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenH264 library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenH264.

%package -n browser-gmp-openh264
Summary:	OpenH264 plugin for Gecko based browsers
Summary(pl.UTF-8):	Wtyczka OpenH264 dla przeglądarek opartych na Gecko
License:	BSD and MPL v2.0
Group:		Libraries
Requires:	browser-plugins >= 2.0

%description -n browser-gmp-openh264
OpenH264 Gecko Media Plugin for modern Gecko based browsers (like
Firefox/Iceweasel 33+).

%description -n browser-gmp-openh264 -l pl.UTF-8
Wtyczka GMP (Gecko Media Plugin) OpenH264 dla nowych przeglądarek
opartych na Gecko (takich jak Firefox/Iceweasel 33+).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%if %{with gmp_api}
ln -s /usr/include/gmp-api gmp-api
%endif

%build
%{__make} libraries binaries %{?with_gmp_api:plugin} \
	ARCH=%{_target_base_arch} \
%ifarch x32
	IS_X32=Yes \
%endif
	CXX="%{__cxx}" \
	CFLAGS_OPT="%{rpmcxxflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR_NAME=%{_lib}

install h264dec h264enc $RPM_BUILD_ROOT%{_bindir}

%if %{with gmp_api}
# see https://wiki.mozilla.org/GeckoMediaPlugins
install -d $RPM_BUILD_ROOT%{gmp_plugindir}/gmp-openh264
install libgmpopenh264.so $RPM_BUILD_ROOT%{gmp_plugindir}/gmp-openh264
cp -p gmpopenh264.info $RPM_BUILD_ROOT%{gmp_plugindir}/gmp-openh264
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n browser-gmp-openh264
%update_browser_plugins

%postun -n browser-gmp-openh264
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS LICENSE README.md RELEASES
%attr(755,root,root) %{_bindir}/h264dec
%attr(755,root,root) %{_bindir}/h264enc
%attr(755,root,root) %{_libdir}/libopenh264.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenh264.so.6

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenh264.so
%{_includedir}/wels
%{_pkgconfigdir}/openh264.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopenh264.a

%if %{with gmp_api}
%files -n browser-gmp-openh264
%defattr(644,root,root,755)
%dir %{gmp_plugindir}/gmp-openh264
%attr(755,root,root) %{gmp_plugindir}/gmp-openh264/libgmpopenh264.so
%{gmp_plugindir}/gmp-openh264/gmpopenh264.info
%endif
