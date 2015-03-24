# TODO: handle GMP plugins better in browser-plugins architecture (only firefox33+ based browsers supported)
#
# Conditional build:
%bcond_without	xulrunner	# GMP plugin
#
Summary:	H.264 codec library
Summary(pl.UTF-8):	Biblioteka kodeka H.264
Name:		openh264
Version:	1.4.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/cisco/openh264/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	06d92ee5bd231814394b7e29f0545e57
Patch0:		%{name}-libdir.patch
URL:		http://www.openh264.org/
BuildRequires:	libstdc++-devel
%ifarch %{ix86} %{x8664}
BuildRequires:	nasm
%endif
BuildRequires:	rpmbuild(macros) >= 1.357
%{?with_xulrunner:BuildRequires:	xulrunner-devel >= 2:33}
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

%if %{with xulrunner}
ln -s /usr/include/xulrunner gmp-api
%endif

%build
%{__make} libraries binaries %{?with_xulrunner:plugin} \
	ARCH=%{_target_base_arch} \
	CXX="%{__cxx}" \
	CFLAGS_OPT="%{rpmcxxflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

install h264dec h264enc $RPM_BUILD_ROOT%{_bindir}

%if %{with xulrunner}
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
%attr(755,root,root) %{_libdir}/libopenh264.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenh264.so
%{_includedir}/wels
%{_pkgconfigdir}/openh264.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopenh264.a

%if %{with xulrunner}
%files -n browser-gmp-openh264
%defattr(644,root,root,755)
%dir %{gmp_plugindir}/gmp-openh264
%attr(755,root,root) %{gmp_plugindir}/gmp-openh264/libgmpopenh264.so
%{gmp_plugindir}/gmp-openh264/gmpopenh264.info
%endif
