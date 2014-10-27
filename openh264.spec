# TODO: GMP plugin
Summary:	H.264 codec library
Summary(pl.UTF-8):	Biblioteka kodeka H.264
Name:		openh264
Version:	1.1
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/cisco/openh264/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2dccd64e0359acbaec54f442792bba67
URL:		http://www.openh264.org/
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q

%build
%{__make} \
	CXX="%{__cxx}" \
	CFLAGS_OPT="%{rpmcxxflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}}

%{__make} install-headers \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

install libopenh264.so libopenh264.a $RPM_BUILD_ROOT%{_libdir}
install h264dec h264enc $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS LICENSE README.md RELEASES
%attr(755,root,root) %{_bindir}/h264dec
%attr(755,root,root) %{_bindir}/h264enc
%attr(755,root,root) %{_libdir}/libopenh264.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/wels

%files static
%defattr(644,root,root,755)
%{_libdir}/libopenh264.a
