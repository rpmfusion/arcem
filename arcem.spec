Name:           arcem
Version:        1.50.2
Release:        5%{?dist}
Summary:        Highly portable Acorn Archimedes emulator

License:        GPLv2+
URL:            http://arcem.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.zip
# ARMLinux Rom Image - kernel v2.2
Source1:        http://arcem.sourceforge.net/linuxrom.zip
# Wrapper script
Source2:        %{name}.sh
# RPM Fusion README
Source3:        README_%{name}.Fedora
# User manual
Source4:        http://arcem.sourceforge.net/manual/%{name}-1.50.html
Source5:        %{name}.desktop
# Appdata by Richard Hughes
# http://sourceforge.net/p/arcem/bugs/18/
Source6:        %{name}.appdata.xml
# Makefile patch
Patch0:         %{name}-1.50-Makefile.patch

BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libicns-utils
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       xorg-x11-apps

%description
ArcEm is a Acorn Archimedes A400 hardware emulator that is highly portable. As
it's a hardware emulator it's capable of running multiple operating systems
including RISC OS 3.XX and ARM Linux. ArcEm requires either a RISC OS 3.XX or
ARM Linux ROM to fully function. Only the Linux ROM can be legally included.


%prep
%setup -qn %{name}-src
# Makefile is heavily patched because it's largely broken in many ways
%patch0 -p1
unzip -qq %{SOURCE1}

# Place the user manual
install -pm0644 %{SOURCE4} manual.html 

# Place RPM Fusion README
install -pm0644 %{SOURCE3} .

# Fix premissions
chmod 644 docs/*
find . -type f -name "*.h" -exec chmod 644 {} \;
find . -type f -name "*.c" -exec chmod 644 {} \;


%build
export CFLAGS="%{optflags}"
make %{?_smp_mflags} SOUND_SUPPORT=yes


%install
make install INSTALL_DIR=%{buildroot} prefix=%{_prefix}

# Install default configuration file
mkdir -p %{buildroot}%{_datadir}/%{name}
install -pm0644 arcemrc %{buildroot}%{_datadir}/%{name}

# Install ARMLinux Rom Image
mkdir -p %{buildroot}%{_datadir}/%{name}/linuxrom
install -pm0644 ROM.linux %{buildroot}%{_datadir}/%{name}/linuxrom/ROM

# Install modules
mkdir -p %{buildroot}%{_datadir}/%{name}/modules
install -pm0644 support_modules/*/*,ffa %{buildroot}%{_datadir}/%{name}/modules

# Install wrapper script
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.bin
install -pm0755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}

# Extract Mac OS X icons
icns2png -x macosx/%{name}.icns 

# Install icons
for i in 128; do
  install -d -m 755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  install -m 644 %{name}_${i}x${i}x32.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install desktop file
install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE5}

# Install appdata
install -d %{buildroot}%{_datadir}/appdata
install -p -m 0644 %{SOURCE6} \
  %{buildroot}%{_datadir}/appdata
appstream-util validate-relax --nonet \
  %{buildroot}%{_datadir}/appdata/*.appdata.xml


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/appdata/%{name}.appdata.xml
%doc docs/5thColumn.txt manual.html README_arcem.Fedora
%license docs/COPYING


%changelog
* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.50.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.50.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.50.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.50.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 11 2017 Andrea Musuruane <musuruan@gmail.com> - 1.50.2-1
- Updated to 1.50.2

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.50.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 05 2016 Andrea Musuruane <musuruan@gmail.com> - 1.50.1-1
- Updated to 1.50.1
- Added appdata thanks to Richard Hughes
- Spec file clean up

* Sat Aug 30 2014 Sérgio Basto <sergio@serjux.com> - 1.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Oct 28 2013 Andrea Musuruane <musuruan@gmail.com> 1.50-2
- Dropped desktop vendor tag for F19+
- Dropped cleaning at the beginning of %%install

* Wed Jan 02 2013 Andrea Musuruane <musuruan@gmail.com> 1.50-1
- Updated to 1.50
- Specfile update and cleanup
- Dropped archs no longer supported by Fedora/RPM Fusion
- Used MacOS X icns instead of the Windows ico

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.10-6.cvs_20070611
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.10-5.cvs_20070611
- rebuild for new F11 features

* Tue Jul 29 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.10-4.cvs_20070611
- rebuild for buildsys cflags issue

* Wed Dec 12 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.10-3.cvs_20070611
- Minor spec changes for devel

* Wed Aug 08 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.10-2.cvs_20070611
- Added patch to fix sound.c compilation on newer GCCs

* Tue Aug 07 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.10-1.cvs_20070611
- Minor cleanups to the SPEC
- Updated license field due to new guidelines

* Mon Jun 11 2007 Ian Chapman <packages@amiga-hardware.com> 1.10-0.cvs_20070611
- Initial Release
