%define version %(cat version)
%if 0%{?qubes_builder}
%define _builddir %(pwd)
%endif
    
Name:		qubes-input-proxy
Version:	%{version}
Release:	1%{?dist}
Obsoletes:	input-proxy
Summary:	Simple input device proxy (receiver)

Group:		System Environment/Daemons
License:	GPLv2
URL:		https://www.qubes-os.org/

BuildRequires:	kernel-headers
BuildRequires:	python-setuptools
BuildRequires:	python3-devel

%description
Simple input device proxy, which pass events from /dev/input/eventN device, to
/dev/uintput. It uses stdin/stdout, so it suitable for use as Qubes RPC service.
This package is receiver part.

%package sender
Summary:    Simple input device proxy (sender)

%description sender
Simple input device proxy, which pass events from /dev/input/eventN device, to
/dev/uintput. It uses stdin/stdout, so it suitable for use as Qubes RPC service.
This package is sender part.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build
make %{?_smp_mflags} all


%install
make install DESTDIR=%{buildroot}

%files
%doc README.md
%defattr(-,root,root,-)
/usr/bin/input-proxy-receiver
/etc/qubes-rpc/qubes.InputMouse
/etc/qubes-rpc/qubes.InputKeyboard
/etc/qubes-rpc/qubes.InputTablet
/lib/udev/rules.d/90-qubes-uinput.rules
/lib/modules-load.d/qubes-uinput.conf
%{python_sitelib}/qubesinputproxy-*.egg-info/*
%{python_sitelib}/qubesinputproxy
%{python3_sitelib}/qubesinputproxy-*.egg-info/*
%{python3_sitelib}/qubesinputproxy
%attr(0664,root,qubes) %config(noreplace) /etc/qubes-rpc/policy/qubes.InputMouse
%attr(0664,root,qubes) %config(noreplace) /etc/qubes-rpc/policy/qubes.InputKeyboard
%attr(0664,root,qubes) %config(noreplace) /etc/qubes-rpc/policy/qubes.InputTablet

%files sender
%doc README.md
%defattr(-,root,root,-)
/etc/sudoers.d/qubes-input-trigger
/usr/bin/input-proxy-sender
/usr/bin/qubes-input-trigger
%config(noreplace) /etc/xdg/autostart/qubes-input-trigger.desktop
/lib/udev/rules.d/90-qubes-input-proxy.rules
%{_unitdir}/qubes-input-sender-tablet@.service
%{_unitdir}/qubes-input-sender-mouse@.service
%{_unitdir}/qubes-input-sender-keyboard@.service
%{_unitdir}/qubes-input-sender-keyboard-mouse@.service

%changelog

