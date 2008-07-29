# The source is retrieved from cvs:
# cvs -z3 -d:pserver:anonymous@arcem.cvs.sourceforge.net:/cvsroot/arcem co -P arcem
# The arcem directory should be compressed as the following:
# arcem-cvs_YYYYMMDD.tar.bz2

%define         cvsdate 20070611

Name:           arcem
Version:        1.10
Release:        4.cvs_%{cvsdate}%{?dist}
Summary:        Highly portable Acorn Archimedes emulator
Group:          Applications/Emulators
License:        GPLv2+
URL:            http://arcem.sourceforge.net
Source0:        %{name}-cvs_%{cvsdate}.tar.bz2
Source1:        http://arcem.sourceforge.net/linuxrom.zip
Source2:        arcem.sh
Source3:        README_arcem.dribble
Patch0:         arcem-cvs_20070611-improvemakefile.patch
Patch1:         arcem-cvs_20070611-uichanges.patch
Patch2:         arcem-cvs_20070611-manual.patch
Patch3:         arcem-cvs_20070611-soundfix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
Requires:       hicolor-icon-theme
Requires:       xorg-x11-apps

%description
ArcEm is a Acorn Archimedes A400 hardware emulator that is highly portable. As
it's a hardware emulator it's capable of running multiple operating systems
including RISC OS 3.XX and ARM Linux. ArcEm requires either a RISC OS 3.XX or
ARM Linux ROM to fully function. Only the Linux ROM can be legally included.


%prep
%setup -qn %{name}
# Makefile is heavily patched because it's largely broken in many ways
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
unzip -qq %{SOURCE1}


%build
# Sound support seems stable but experimental, but largely doesn't work on PPC
%ifarch %{ix86} x86_64
    make %{?_smp_mflags} RPMFLAGS="%{optflags}" SOUND_SUPPORT=yes
%else
    make %{?_smp_mflags} RPMFLAGS="%{optflags}" HOST_BIGENDIAN=yes
%endif

#Build icon image
convert win/arc.ico %{name}.png

# Build desktop icon
cat >%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=Arcem
GenericName=Acorn Archimedes Emulator
Comment=%{summary}
Exec=%{name} auto
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;Emulator;
EOF


%install
rm -rf %{buildroot}
make install INSTALL_DIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}/{modules,linuxrom}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -pm0644 support_modules/*/*,ffa %{buildroot}%{_datadir}/%{name}/modules
install -pm0644 ROM.linux %{buildroot}%{_datadir}/%{name}/linuxrom/ROM
install -pm0755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}
install -pm0644 %{name}-0.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -pm0644 %{SOURCE3} .
desktop-file-install --vendor dribble \
    --dir %{buildroot}%{_datadir}/applications \
    %{name}.desktop


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{_datadir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc docs/5thColumn.txt docs/COPYING index.html manual.html README_arcem.dribble


%changelog
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