Summary:	Internet Daemon: Authorization, User Identification
Summary(de):	Internet-D�mon: Autorisierung, User-Identifikation
Summary(fr):	D�mon Internet : autorisation, identification de l'utilisateur
Summary(pl):	Demon Internetowy: autoryzacja, identyfikacja u�ytkownika
Summary(tr):	Internet kullan�c� saptama s�reci
Name:		pidentd
Version:	3.1a22
Release:	2
License:	Public Domain
Group:		Networking/Daemons
Source0:	ftp://ftp.lysator.liu.se/pub/ident/servers/test/%{name}-%{version}.tar.gz
# Source0-md5:	943493b93d97db6322435810b22b0618
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
BuildRequires:	autoconf
Prereq:		rc-inetd >= 0.8.1
Provides:	identserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	linux-identd
Obsoletes:	linux-identd-inetd
Obsoletes:	linux-identd-standalone
Obsoletes:	oidentd

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
d'identication. Il agit en regardant des connexions TCP/IP sp�cifiques
et en renvoyant le nom de l'utilisateur du processus qui poss�de la
connexion.

%description -l pl
Identd jest programem zgodnym z RFC1413 (serwer identyfikacji). Demon
ten sprawdza po��czenia TCP/IP i weryfikuje nazw� u�ytkownika procesu
kt�ry tworzy po��czenie.

Gdy u�ywasz pidentda w wersji wykorzystuj�cej w�tki (threads) pami�taj
o uruchamianiu go z inetd w trybie 'wait'.

%description -l tr
identd RFC1413 ile tan�mlanm�� sunucuyu ger�ekleyen bir programd�r.
Ba�lant� kuran s�recin kullan�c� ismini geri d�nd�r�r.

%prep
%setup  -q
%patch0 -p1

%build
#autoconf
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install DESTDIR=$RPM_BUILD_ROOT

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
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/identd.conf
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/rc-inetd/pidentd
%{_mandir}/man*/*
