Summary:	Internet Daemon: Authorization, User Identification
Summary(de):	Internet-Dämon: Autorisierung, User-Identifikation 
Summary(fr):	Démon Internet : autorisation, identification de l'utilisateur
Summary(pl):	Demon Internetowy: autoryzacja, identyfikacja u¿ytkownika
Summary(tr):	Internet kullanýcý saptama süreci
Name:		pidentd
Version:	3.1a14
Release:	6
Copyright:	Public domain
Group:		Networking
Group(pl):	Sieciowe
Source0:	ftp://ftp.lysator.liu.se/pub/ident/servers/test/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		http://www.imasy.or.jp/~ume/ipv6/pidentd-3.1a14-ipv6-based-on-19990720.diff
Patch1:		pidentd-DESTDIR.patch
Patch2:		pident-ip6-ip4-fix.patch
Prereq:		rc-inetd >= 0.8.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

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
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p0

%build
autoconf
%configure \
	--with-threads 	\
	--enable-ipv6
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

make install DESTDIR=$RPM_BUILD_ROOT

install etc/identd.conf $RPM_BUILD_ROOT%{_sysconfdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/pidentd

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* ChangeLog FAQ README TODO doc/rfc1413.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc {ChangeLog,FAQ,README,TODO,doc/rfc1413.txt}.gz
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/identd.conf
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/rc-inetd/pidentd
