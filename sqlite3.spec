%define		upstream_ver	3081002

Summary:	SQLite library
Name:		sqlite3
Version:	3.8.10.2
Release:	1
License:	LGPL
Group:		Libraries
# Source0Download: http://sqlite.org/download.html
Source0:	http://www.sqlite.org/2015/sqlite-src-%{upstream_ver}.zip
# Source0-md5:	5d717638b97b3be1a4d855d957028738
URL:		http://sqlite.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcl
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexiblity of an SQL database without the administrative hassles of
supporting a separate database server. Because it omits the
client-server interaction overhead and writes directly to disk, SQLite
is also faster than the big database servers for most operations. In
addition to the C library, the SQLite distribution includes a
command-line tool for interacting with SQLite databases and SQLite
bindings for Tcl/Tk.

%package devel
Summary:	Header files for SQLite development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files needed to develop programs that
use these SQLite.

%prep
%setup -qn sqlite-src-%{upstream_ver}

%{__sed} -i 's/mkdir doc/#mkdir doc/' Makefile*

%build
%{__libtoolize}
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure \
	--disable-tcl		\
	--enable-load-extension	\
	--enable-static=no	\
	--enable-threadsafe

%{__make} \
	OPT_FEATURE_FLAGS="\
	-DSQLITE_ENABLE_COLUMN_METADATA=1	\
	-DSQLITE_ENABLE_FTS3=1			\
	-DSQLITE_ENABLE_RTREE=1			\
	-DSQLITE_ENABLE_UNLOCK_NOTIFY=1		\
	-DSQLITE_SECURE_DELETE=1"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install sqlite3.1 $RPM_BUILD_ROOT%{_mandir}/man1

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/sqlite3
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_mandir}/man1/sqlite3.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h
%{_pkgconfigdir}/*.pc

