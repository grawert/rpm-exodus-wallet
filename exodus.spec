%global debug_package %{nil}

Name:           exodus
Version:        26.3.11
Release:        1%{?dist}
Summary:        Exodus cryptocurrency wallet
License:        Proprietary
URL:            https://www.exodus.com
Source0:        exodus-linux-x64-%{version}.zip
Source1:        exodus.svg

ExclusiveArch:  x86_64

AutoReqProv:    no

Requires:       libX11
Requires:       libXcomposite
Requires:       libXcursor
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXi
Requires:       libXrandr
Requires:       libXrender
Requires:       libXtst
Requires:       libxcb
Requires:       libxkbcommon
Requires:       alsa-lib
Requires:       at-spi2-atk
Requires:       atk
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk3
Requires:       mesa-libEGL
Requires:       nss
Requires:       nspr
Requires:       pango

%description
Exodus is a multi-asset cryptocurrency wallet with a built-in exchange,
portfolio tracker, and hardware wallet support. This package installs the
Exodus desktop application for Linux (x86_64).

%prep
%setup -q -n Exodus-linux-x64

%build
# Pre-built Electron application — nothing to compile.

%install
install -d %{buildroot}/opt/exodus
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

cp -a . %{buildroot}/opt/exodus/

# Remove the upstream desktop file and install script; we handle those below.
rm -f %{buildroot}/opt/exodus/exodus.desktop
rm -f %{buildroot}/opt/exodus/install-desktop-file.sh

# Add application icon
install -m 644 %{_sourcedir}/exodus.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/exodus.svg

# Ensure correct permissions — no setuid; user namespaces handle sandboxing.
chmod 755 %{buildroot}/opt/exodus/Exodus
chmod 755 %{buildroot}/opt/exodus/chrome-sandbox

# Wrapper script in PATH — tries user namespaces, falls back to --no-sandbox
# on kernels where unprivileged user namespaces are disabled.
cat > %{buildroot}%{_bindir}/exodus <<'EOF'
#!/bin/sh
if [ "$(cat /proc/sys/user/max_user_namespaces 2>/dev/null)" = "0" ]; then
    exec /opt/exodus/Exodus --no-sandbox "$@"
else
    exec /opt/exodus/Exodus "$@"
fi
EOF
chmod 755 %{buildroot}%{_bindir}/exodus

# Desktop entry
cat > %{buildroot}%{_datadir}/applications/exodus.desktop <<'EOF'
[Desktop Entry]
Name=Exodus
Comment=Exodus Cryptocurrency Wallet
Exec=/opt/exodus/Exodus %U
Icon=exodus
Terminal=false
Type=Application
Categories=Finance;Network;
StartupWMClass=Exodus
MimeType=x-scheme-handler/exodus;
EOF

%post
update-desktop-database %{_datadir}/applications &>/dev/null || :
xdg-mime default exodus.desktop x-scheme-handler/exodus &>/dev/null || :
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database %{_datadir}/applications &>/dev/null || :
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license /opt/exodus/LICENSE
/opt/exodus/LICENSES.chromium.html

# Binaries / sandbox
%attr(755, root, root) /opt/exodus/Exodus
%attr(755, root, root) /opt/exodus/chrome-sandbox
%attr(755, root, root) /opt/exodus/chrome_crashpad_handler

# Electron / Chromium runtime
/opt/exodus/chrome_100_percent.pak
/opt/exodus/chrome_200_percent.pak
/opt/exodus/icudtl.dat
/opt/exodus/resources.pak
/opt/exodus/snapshot_blob.bin
/opt/exodus/v8_context_snapshot.bin
/opt/exodus/version
/opt/exodus/vk_swiftshader_icd.json

# Bundled shared libraries
/opt/exodus/libEGL.so
/opt/exodus/libffmpeg.so
/opt/exodus/libGLESv2.so
/opt/exodus/libvk_swiftshader.so
/opt/exodus/libvulkan.so.1

# Application resources and locales
/opt/exodus/resources/
/opt/exodus/locales/

# System integration
%{_bindir}/exodus
%{_datadir}/applications/exodus.desktop
%{_datadir}/icons/hicolor/scalable/apps/exodus.svg

%changelog
* Tue Mar 17 2026 Uwe Grawert <uwe.grawert@linked-planet.com> - 26.3.11-1
- Update Exodus to version 26.3.11
