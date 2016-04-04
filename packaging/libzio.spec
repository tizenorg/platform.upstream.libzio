Name:           libzio
Version:        0.99
Release:        0
License:        GPL-2.0+
Summary:        A Library for Accessing Compressed Text Files
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	libzio.manifest
BuildRequires:  bzip2-devel
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

%description
Libzio provides a wrapper function for reading or writing gzip or bzip2
files with FILE streams.

%package        devel
Summary:        Libzio development files
Group:          Development/Libraries/C and C++
Requires:       libzio = %{version}

%description    devel
Libzio development files including zio.h, the manual page fzopen(3),
and static library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS+=" -fvisibility=hidden"
  export CXXFLAGS+=" -fvisibility=hidden"
  
make %{?_smp_mflags} noweak

%check
make testt
make tests
for comp in gzip bzip2 lzma xz
do
    $comp -c < fzopen.3.in > fzopen.test
    ./testt fzopen.test | cmp fzopen.3.in -
    cat fzopen.test | ./tests ${comp:0:1} | cmp fzopen.3.in -
done

%install
make DESTDIR=%{buildroot} install libdir=%{_libdir} mandir=%{_mandir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libzio.so.0
%{_libdir}/libzio.so.%{version}

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%doc README COPYING
%{_libdir}/libzio.a
%{_libdir}/libzio.so
%{_mandir}/man3/fzopen.3*
/usr/include/zio.h

%changelog
