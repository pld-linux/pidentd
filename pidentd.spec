Summary:     Internet Daemon: Authorization, User Identification
Name:        pidentd
Version:     3.0.4
Release:     1
URL:         ftp://ftp.lysator.liu.se/pub/ident/servers
Source:      %{name}-%{version}.tar.gz
Copyright:   Public domain
Group:       Networking
Group(pl):   Sieci
BuildRoot:   /tmp/%{name}-%{version}-%{release}-root
Summary(de): Internet-Dämon: Autorisierung, User-Identifikation 
Summary(fr): Démon Internet : autorisation, identification de l'utilisateur
Summary(pl): Demon Iternetowy: autoryzacja, identyfikacja u¿ytkownika
Summary(tr): Internet kullanýcý saptama süreci

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

%description -l tr
identd RFC1413 ile tanýmlanmýþ sunucuyu gerçekleyen bir programdýr. Baðlantý
kuran sürecin kullanýcý ismini geri döndürür.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -w" LDFLAGS=-s \
	./configure \
	--with-threads \
	--prefix=/usr \
	--sysconfdir=/etc \
	--mandir=/usr/share/man 
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{usr/{sbin,share/man/man8},etc}
make prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_BUILD_ROOT/etc mandir=$RPM_BUILD_ROOT/usr/share/man install

install etc/identd.conf $RPM_BUILD_ROOT/etc

bzip2 -9 $RPM_BUILD_ROOT/usr/share/man/man8/* ChangeLog FAQ README Y2K TODO doc/rfc1413.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.bz2 FAQ.bz2 README.bz2 Y2K.bz2 TODO.bz2 doc/rfc1413.txt.bz2

%attr(711,root,root) /usr/sbin/*
%attr(644,root, man) /usr/share/man/man8/*
%config(noreplace) %verify(not mtime md5 size) /etc/identd.conf
