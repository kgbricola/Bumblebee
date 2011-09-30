
%global	       debug_package %{nil}
%global	       __strip /bin/true

Name:            acpi_call-kmod-common

Epoch:           1
Version:         1
Release:         1%{?dist}
Summary:         Test for acpi_call
Group:           System Environment/Kernel
License:         GPL
URL:             https://github.com/mkottman/acpi_call.git
Source0:         acpi_call.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:        acpi_call-kmod-common = %{?epoch}:%{version}
#Requires:        %{name} = %{?epoch}:%{version}-%{release}

ExclusiveArch: i686 x86_64

%description
This package provides the acpi_call common.

%prep
%setup -q -c -T -a 0

%build
#nothing to do

%install
rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 test_off.sh $RPM_BUILD_ROOT%{_bindir}/test_off.sh


%files
%defattr(-,root,root,-)
%{_bindir}/test_off.sh

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Sep 23 2011 Rico Schüller <kgbricola@web.de>
- Initial release.
