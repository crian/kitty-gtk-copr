# Source build of https://github.com/taiwbi/kitty (kitty fork with GTK4/libadwaita
# frontend, Arabic support and font cut-off fixes), derived from Fedora's kitty.spec.

%global debug_package %{nil}
%global upstream_tag v.%{version}
%global base_version 0.49.2

Name:           kitty-gtk
Version:        0.49.2.15
Release:        1%{?dist}
Summary:        GPU-accelerated terminal emulator (taiwbi fork with GTK4 UI and Arabic support)

License:        GPL-3.0-only AND LGPL-2.1-or-later AND Zlib AND MIT AND CC0-1.0 AND BSD-2-Clause AND BSD-3-Clause AND Apache-2.0 AND MPL-2.0
URL:            https://github.com/taiwbi/kitty
Source0:        %{url}/releases/download/%{upstream_tag}/kitty-%{base_version}.tar.xz
Source1:        https://github.com/ryanoasis/nerd-fonts/releases/latest/download/NerdFontsSymbolsOnly.tar.xz

ExcludeArch:    %{ix86}

BuildRequires:  golang >= 1.26.0
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  lcms2-devel
BuildRequires:  ncurses
BuildRequires:  wayland-devel
BuildRequires:  simde-static
BuildRequires:  shader-slang-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(cairo-fc)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4

Requires:       python3%{?_isa}
Requires:       hicolor-icon-theme
Requires:       python3-gobject
Requires:       python3-cairo
Requires:       gtk4
Requires:       libadwaita >= 1.4
Recommends:     shader-slang
Recommends:     ripgrep
Suggests:       ImageMagick

# Drop-in replacement for Fedora's kitty
Provides:       kitty = %{version}-%{release}
Provides:       kitty-kitten = %{version}-%{release}
Provides:       kitty-terminfo = %{version}-%{release}
Provides:       kitty-shell-integration = %{version}-%{release}
Conflicts:      kitty
Conflicts:      kitty-kitten
Conflicts:      kitty-terminfo
Conflicts:      kitty-shell-integration

Provides:       bundled(glfw)
Provides:       bundled(c-ringbuf)
Provides:       bundled(base64simd)
Provides:       bundled(font(SymbolsNFM))

%description
Fork of kitty, the fast, feature-rich, GPU-based terminal emulator, with a
GTK4/libadwaita frontend, Arabic text support and fixes for cut-off fonts.

Includes the kitten helper, the terminfo entry and the shell integration scripts.

%prep
%setup -q -c -T -n %{name}-%{version}
tar -xJf %{SOURCE0} --strip-components=1
mkdir fonts
tar -xf %{SOURCE1} -C fonts

# Make shebangs Fedora-compatible
find -type f -name "*.py" -exec sed -e 's|/usr/bin/env python3|%{python3}|g' \
    -e 's|/usr/bin/env python|%{python3}|g' \
    -e 's|/usr/bin/env -S kitty|/usr/bin/kitty|g' \
    -i "{}" \;


%build
%set_build_flags
export KITTY_REQUIRE_GTK=1
export GOTOOLCHAIN=local
export GOPATH=%{_builddir}/gopath
export GOFLAGS=-buildvcs=false

# builds kitty and kitten
%{python3} setup.py linux-package \
    --libdir-name=%{_lib} \
    --update-check-interval=0 \
    --verbose \
    --ignore-compiler-warnings

%install
# rpmlint fixes
find linux-package -type f ! -executable -name "*.py" -exec sed -i '1{\@^#!%{python3}@d}' "{}" \;
find linux-package/%{_lib}/kitty/shell-integration -type f ! -executable -exec sed -r -i '1{\@^#!/bin/(fish|zsh|sh|bash)@d}' "{}" \;

cp -r linux-package %{buildroot}%{_prefix}
find %{buildroot}%{_docdir}/kitty -name .buildinfo -delete

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%license LICENSE
%{_bindir}/kitty
%{_bindir}/kitten
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.{png,svg}
%{_datadir}/terminfo/x/xterm-kitty
%{_libdir}/kitty/
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_docdir}/kitty/

%changelog
* Fri Oct 30 2026 crian <crian84@gmail.com> - 0.49.2.15-1
- Initial source build of taiwbi/kitty v.0.49.2.15
