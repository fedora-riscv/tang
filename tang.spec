Name:           tang
Version:        3
Release:        1%{?dist}
Summary:        Network Presence Binding Daemon

License:        GPLv3+
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  jose >= 5
BuildRequires:  libjose-devel >= 5
BuildRequires:  libjose-zlib-devel >= 5
BuildRequires:  libjose-openssl-devel >= 5

BuildRequires:  http-parser-devel >= 2.7.1-3
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig

BuildRequires:  systemd
BuildRequires:  wget

BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  sed

%{?systemd_requires}
Requires:       coreutils
Requires:       jose >= 5
Requires:       grep
Requires:       sed

Requires(pre):  shadow-utils

%description
Tang is a small daemon for binding data to the presence of a third party.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT
%make_install
%{__sed} -i 's|DirectoryMode=0700||' $RPM_BUILD_ROOT/%{_unitdir}/%{name}d-update.path
%{__sed} -i 's|MakeDirectory=true||' $RPM_BUILD_ROOT/%{_unitdir}/%{name}d-update.path
echo "User=%{name}" >> $RPM_BUILD_ROOT/%{_unitdir}/%{name}d-update.service
echo "User=%{name}" >> $RPM_BUILD_ROOT/%{_unitdir}/%{name}d@.service
%{__mkdir_p} $RPM_BUILD_ROOT/%{_localstatedir}/cache/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_localstatedir}/db/%{name}

%check
if ! make %{?_smp_mflags} check; then
    cat test-suite.log
    false
fi

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_localstatedir}/cache/%{name} -s /sbin/nologin \
    -c "Tang Network Presence Daemon user" %{name}
exit 0

%post
%systemd_post %{name}d.socket
%systemd_post %{name}d-update.path

%preun
%systemd_preun %{name}d.socket
%systemd_preun %{name}d-update.path

%postun
%systemd_postun_with_restart %{name}d.socket
%systemd_postun_with_restart %{name}d-update.path

%files
%license COPYING
%attr(0750, %{name}, %{name}) %{_localstatedir}/cache/%{name}
%attr(2570, %{name}, %{name}) %{_localstatedir}/db/%{name}
%{_unitdir}/%{name}d-update.service
%{_unitdir}/%{name}d-update.path
%{_unitdir}/%{name}d@.service
%{_unitdir}/%{name}d.socket
%{_libexecdir}/%{name}d-update
%{_libexecdir}/%{name}d

%changelog
* Wed Oct 26 2016 Nathaniel McCallum <npmccallum@redhat.com> - 3-1
- New upstream release

* Wed Oct 19 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2-1
- New upstream release

* Tue Aug 23 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1-1
- First release
