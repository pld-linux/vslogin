Summary:	Virtual Server Login
Name:		vslogin
Version:	0
Release:	0.1
License:	public domain
Group:		Base
Source0:	http://dev.call2ru.com/vserverauth.tar.gz
# Source0-md5:	ff76f401ece80d9f01b5cd990ec71ed1
Patch0:		%{name}-make.patch
URL:		http://linux-vserver.org/HowtoSSHLogin
Requires(post):	grep
Requires(post,preun):	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir		/sbin
%define		_shellname		%{_sbindir}/vslogin
%define		_shellsfile		/etc/shells

%description
vslogin allows virtual users to log directly in to their vserver, scp,
etc.

%prep
%setup -q -n vserverauth
%patch0 -p1

%build
%{__make} -C vslogin \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install vslogin/vslogin $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_shellsfile} ]; then
	umask 002
	echo '%{_shellname}' >> %{_shellsfile}
else
	grep -q '^%{_shellname}$' %{_shellsfile} || echo '%{_shellname}' >> %{_shellsfile}
fi

%preun
if [ "$1" = "0" ]; then
	sed -i -e '/^%(echo %{_shellname} | sed -e 's,/,\\/,g')$/d' %{_shellsfile}
fi

%files
%defattr(644,root,root,755)
%doc readme
%attr(755,root,root) %{_sbindir}/vslogin
