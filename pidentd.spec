Summary:	Internet Daemon: Authorization, User Identification
Summary(de):	Internet-Dämon: Autorisierung, User-Identifikation
Summary(fr):	Démon Internet : autorisation, identification de l'utilisateur
Summary(pl):	Demon Internetowy: autoryzacja, identyfikacja u¿ytkownika
Summary(tr):	Internet kullanýcý saptama süreci
Name:		pidentd
Version:	3.1a25
Release:	3
License:	Public Domain
Group:		Networking/Daemons
Source0:	ftp://ftp.lysator.liu.se/pub/ident/servers/test/%{name}-%{version}.tar.gz
# Source0-md5:	cdb1a8a9d881233cf52400d4f0e3a6e1
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-ac_fix.patch
Patch2:		%{name}-segv.patch
Patch3:		%{name}-config.patch
URL:		http://www.lysator.liu.se/~pen/pidentd/
BuildRequires:	autoconf
BuildRequires:	automake
Requires:	rc-inetd >= 0.8.1
Provides:	identserver
Obsoletes:	linux-identd
Obsoletes:	linux-identd-inetd
Obsoletes:	linux-identd-standalone
Obsoletes:	midentd
Obsoletes:	oidentd
Obsoletes:	oidentd-inetd
Obsoletes:	oidentd-standalone
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
identd is a program that implements the RFC1413 identification server.
identd operates by looking up specific TCP/IP connections and
returning the user name of the process owning the connection.

%description -l de
identd ist ein Programm, das den RFC1413-Identifikations-Server
implementiert. identd untersucht bestimmte TCP/IP-Verbindungen und
gibt dann den Benutzernamen des Prozesses aus, der die Verbindung
besitzt.

%description -l fr
identd est un programme qui implante le RFC1413 serveur
d'identication. Il agit en regardant des connexions TCP/IP spécifiques
et en renvoyant le nom de l'utilisateur du processus qui possède la
connexion.

%description -l pl
Identd jest programem zgodnym z RFC1413 (serwer identyfikacji). Demon
ten sprawdza po³±czenia TCP/IP i weryfikuje nazwê u¿ytkownika procesu
który tworzy po³±czenie.

Gdy u¿ywasz pidentda w wersji wykorzystuj±cej w±tki (threads) pamiêtaj
o uruchamianiu go z inetd w trybie 'wait'.

%description -l tr
identd RFC1413 ile tanýmlanmýþ sunucuyu gerçekleyen bir programdýr.
Baðlantý kuran sürecin kullanýcý ismini geri döndürür.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cp -f /usr/share/automake/config.* aux
cp -f /usr/share/automake/config.* plib/aux
cd plib
%{__autoconf}
%{__autoheader}
cd ..
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install etc/identd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/pidentd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ README TODO
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/identd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/pidentd
%{_mandir}/man*/*
