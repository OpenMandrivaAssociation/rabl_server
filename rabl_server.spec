Summary:	Reactive Autonomous Blackhole List (RABL) Project server
Name:		rabl_server
Version:	1.0.0
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://www.nuclearelephant.com/projects/rabl/
Source0:	http://www.nuclearelephant.com/projects/rabl/sources/%{name}-%{version}.tar.bz2
Source1:	rabl_server.init.bz2
Patch0:		rabl_server-1.0.0-mdv_conf.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	bind
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The RABL (pronounced "rabble") server is a statistical, machine-automated
and up-to-the-second blackhole list server designed to monitor global network
activity and make decisions based on network spread and infection rate - that
is, abuse from an address which has been provided via automated feed from a
number of participating networks. This is in far contrast to how most other
blacklists function, where fallable humans (many with political agendas) must
process thousands of hand-written reports and make decisions - many times after
the fact. The RABL is fully reactive to new threats and can block addresses
within seconds of widespread infection because it is in constant communication
with the participating networks (or "sources") - good to know in this world of
drone PCs and stolen accounts. The RABL server blacklists addresses until they
have cleared a minimum duration (an hour by default) without any additional
reporting, making the appeals process as simple as "fix your junk". The RABL is
designed to function via automated machine-learning spam filters, such as
Bayesian filters. Each participating network is granted write authentication in
the blackhole list, to prevent abuse. A client tool is also provided. Because
no humans are involved in this process, the RABL acts as a mere activity
monitor and can run on its own. There's also nobody to sue (since you can't sue
computers for talking to each other) which makes things far less messy for
participants.

%prep

%setup -q
%patch0 -p0

bzcat %{SOURCE1} > rabl_server.init

%build

%configure2_5x \
    --enable-warnings

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_initrddir}
#install -d %{buildroot}%{_var}/log/rabl_server
#install -d %{buildroot}%{_var}/run/rabl_server

install -m0755 rabl_server %{buildroot}%{_sbindir}/
install -m0755 rabl_server.init %{buildroot}%{_initrddir}/rabl_server
install -m0644 rabl_server.conf %{buildroot}%{_sysconfdir}/

#%pre
#%_pre_useradd rabl_server %{_localstatedir}/rabl_server /bin/sh

%post
%_post_service rabl_server

%preun
%_preun_service rabl_server

#%postun
#%_postun_userdel rabl_server

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGE LICENSE README RELEASE.NOTES
%attr(0755,root,root) %{_initrddir}/rabl_server
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/rabl_server.conf
%attr(0755,root,root) %{_sbindir}/rabl_server
#%attr(0755,named,named) %dir %{_var}/run/rabl_server
#%attr(0755,named,named) %dir %{_var}/log/rabl_server
