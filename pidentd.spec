Summary:	Internet Daemon: Authorization, User Identification
Summary(de):	Internet-D�mon: Autorisierung, User-Identifikation 
Summary(fr):	D�mon Internet : autorisation, identification de l'utilisateur
Summary(pl):	Demon Internetowy: autoryzacja, identyfikacja u�ytkownika
Summary(tr):	Internet kullan�c� saptama s�reci
Name:		pidentd
Version:	3.1a14
Release:	1
Group:		Networking
Group(pl):	Sieciowe
Copyright:	Public domain
Source0:	ftp://ftp.lysator.liu.se/pub/ident/servers/test/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		http://www.imasy.or.jp/~ume/ipv6/pidentd-3.1a14-ipv6-based-on-19990720.diff
Patch1:		pidentd-DESTDIR.patch
Requires:	inetdaemon
Requires:	rc-inetd
BuildRoot:	/tmp/%{name}-%{version}-%{release}-root

%define		_sysconfdir	/etc

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
Il agit en regardant des connexions TCP/IP sp�cifiques et en renvoyant le
nom de l'utilisateur du processus qui poss�de la connexion.

%description -l pl
Identd jest programem zgodnym z RFC1413 (serwer identyfikcji). Demon ten 
sprawdza po��czenia TCP/IP i weryfikuje nazw� u�ytkownika procesu kt�ry
tworzy po��czenie. 

Gdy u�ywasz pidentda w wersji wykorzystuj�cej w�tki (threads) pami�taj
o uruchamianiu go z inetd w trybie 'wait'.

%description -l tr
identd RFC1413 ile tan�mlanm�� sunucuyu ger�ekleyen bir programd�r. Ba�lant�
kuran s�recin kullan�c� ismini geri d�nd�r�r.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

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

install etc/identd.conf $RPM_BUILD_ROOT/etc

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/pidentd

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* ChangeLog FAQ README Y2K TODO doc/rfc1413.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post
/etc/rc.d/init.d/rc-inetd restart >&2

%postun
if [ "$1" = "0" ] ; then
	/etc/rc.d/init.d/rc-inetd restart >&2
fi

%files
%defattr(644,root,root,755)
%doc {ChangeLog,FAQ,README,Y2K,TODO,doc/rfc1413.txt}.gz
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
%config(noreplace) %verify(not mtime md5 size) /etc/identd.conf
%attr(640,root,root) /etc/sysconfig/rc-inetd/pidentd
