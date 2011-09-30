#%define buildforkernels newest
%define buildforkernels current
#define buildforkernels akmods

Name:            acpi_call-kmod
Epoch:           1
Version:         1
Release:         1%{?dist}
Summary:         acpi call kernel modul
Group:           System Environment/Kernel
License:         GPL
URL:             https://github.com/mkottman/acpi_call.git
Source0:         acpi_call.tar.gz

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   redhat-rpm-config
Provides:        acpi_call-kmod
Provides:        acpi_call-kmod-common = %{?epoch}:%{version}

ExclusiveArch: i686 x86_64

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package provides the acpi_call kernel module for kernel %{kversion}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%setup -q -c -T -a 0
#directory fixup
cd .. && mkdir %{name} && mv %{name}-%{version} %{name} && mv %{name} %{name}-%{version} && cd %{name}-%{version}
for kernel_version in %{?kernel_versions} ; do
    cp -a %{name}-%{version} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
#    make install DESTDIR=${RPM_BUILD_ROOT} KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
     install -D -m 755 _kmod_build_${kernel_version%%___*}/acpi_call.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/acpi_call.kmod
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Sep 23 2011 Rico Schüller <kgbricola@web.de>
- Initial release.
