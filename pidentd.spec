Summary:     Internet Daemon: Authorization, User Identification
Summary(de): Internet-Dämon: Autorisierung, User-Identifikation 
Summary(fr): Démon Internet : autorisation, identification de l'utilisateur
Summary(pl): Demon Internetowy: autoryzacja, identyfikacja u¿ytkownika
Summary(tr): Internet kullanýcý saptama süreci
Name:        pidentd
Version:     3.1a14
Release:     1
URL:         ftp://ftp.lysator.liu.se/pub/ident/servers
Source0:     %{name}-%{version}.tar.gz
Source1:     %{name}.inetd
#IPv6 patch: http://www.imasy.or.jp/~ume/ipv6/
Patch:	     pidentd-3.1a14-ipv6-based-on-19990720.diff
Copyright:   Public domain
Group:       Networking
Group(pl):   Sieciowe
BuildRoot:   /tmp/%{name}-%{version}-%{release}-root

%description
identd is a program that implements the RFC1413 identification server.
identd operates by looking up specific TCP/IP connections and
returning the user name of the process owning the connection.

%description -l de
identd ist ein Programm, das den RFC1413-Identifikations-Server
implementiert. identd untersucht bestimmte TCP/IP-Verbindungen
und gibt dann den Benutzernamen des Prozesses aus, der die Verbindung besitzt.

%description -l fr
identd est un programme qui implante le RFC1413 serveur d'identication.
Il agit en regardant des connexions TCP/IP spécifiques et en renvoyant le
nom de l'utilisateur du processus qui possède la connexion.

%description -l pl
Identd jest programem zgodnym z RFC1413 (serwer identyfikcji). Demon ten 
sprawdza po³±czenia TCP/IP i weryfikuje nazwê u¿ytkownika procesu który
tworzy po³±czenie. 

Gdy u¿ywasz pidentda w wersji wykorzystuj±cej w±tki (threads) pamiêtaj
o uruchamianiu go z inetd w trybie 'wait'.

%description -l tr
identd RFC1413 ile tanýmlanmýþ sunucuyu gerçekleyen bir programdýr. Baðlantý
kuran sürecin kullanýcý ismini geri döndürür.

%prep
%setup -q
%patch -p1

%build
autoconf
%configure \
	--with-threads 	\
	--enable-ipv6 \
	--sysconfdir=/etc
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{usr/{sbin,share/man/man8},etc,etc/sysconfig/rc-inetd}
make	prefix=$RPM_BUILD_ROOT%{_prefix} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	sysconfdir=$RPM_BUILD_ROOT/etc \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	install

install etc/identd.conf $RPM_BUILD_ROOT/etc

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/pidentd

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* ChangeLog FAQ README Y2K TODO doc/rfc1413.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {ChangeLog,FAQ,README,Y2K,TODO,doc/rfc1413.txt}.gz
%attr(755,root,root) %{_sbindir}/*
%attr(644,root,root) %{_mandir}/man*/*
%attr(644,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/identd.conf
%attr(640,root,root) /etc/sysconfig/rc-inetd/pidentd
