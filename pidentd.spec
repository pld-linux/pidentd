Summary:     Internet Daemon: Authorization, User Identification
Name:        pidentd
Version:     3.0.1
Release:     1d
URL:         ftp://ftp.lysator.liu.se/pub/ident/servers
Source:      %{name}-%{version}.tar.gz
Copyright:   Public domain
Group:       Networking
Group(pl):   Sieci
BuildRoot:   /tmp/%{name}-%{version}-%{release}-root
Summary(de): Internet-D�mon: Autorisierung, User-Identifikation 
Summary(fr): D�mon Internet : autorisation, identification de l'utilisateur
Summary(pl): Demon Iternetowy: autoryzacja, identyfikacja u�ytkownika
Summary(tr): Internet kullan�c� saptama s�reci

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

%description -l tr
identd RFC1413 ile tan�mlanm�� sunucuyu ger�ekleyen bir programd�r. Ba�lant�
kuran s�recin kullan�c� ismini geri d�nd�r�r.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -w" LDFLAGS=-s \
	./configure \
	--with-threads \
	--prefix=/usr \
	--sysconfdir=/etc
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{usr/{sbin,man/man8},etc}
make prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_BUILD_ROOT/etc install

install etc/identd.conf $RPM_BUILD_ROOT/etc

bzip2 -9 $RPM_BUILD_ROOT/usr/man/man8/* ChangeLog FAQ README Y2K

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.bz2 FAQ.bz2 README.bz2 Y2K.bz2

%attr(711,root,root) /usr/sbin/ide*
%attr(644,root, man) /usr/man/man8/ide*
%config(noreplace) %verify(not mtime md5 size) /etc/identd.conf

%changelog
* Fri Jan 15 1999 Arkadiusz Mi�kiewicz <misiek@misiek.eu.org>
[3.0.1-1d]
- new upstream release

* Mon Nov 09 1998 Wojtek �lusarczyk <wojtek@shadow.eu.org>
[2.7-1d]
- translation modified for pl,
- build for PLD Tornado,
- major changes.

* Mon Aug 17 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 2.7

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
