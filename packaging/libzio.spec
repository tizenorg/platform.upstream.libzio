#
# spec file for package libzio
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           libzio
Version:        0.99
Release:        0
License:        GPL-2.0+
Summary:        A Library for Accessing Compressed Text Files
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
BuildRequires:  bzip2-devel
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Libzio provides a wrapper function for reading or writing gzip or bzip2
files with FILE streams.

%package        devel
Summary:        Libzio development files
Group:          Development/Libraries/C and C++
Requires:       libzio = %{version}
# bug437293
%ifarch ppc64
Obsoletes:      libzio-devel-64bit
%endif
#

%description    devel
Libzio development files including zio.h, the manual page fzopen(3),
and static library.

%prep
%setup -q

%build
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
%defattr(-,root,root)
%{_libdir}/libzio.so.0
%{_libdir}/libzio.so.%{version}

%files devel
%defattr(-,root,root)
%doc README COPYING
%{_libdir}/libzio.a
%{_libdir}/libzio.so
%{_mandir}/man3/fzopen.3*
/usr/include/zio.h

%changelog
