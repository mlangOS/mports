pkgname = "kitty"
pkgver = "0.31"
pkgrel = 1
build_style = "python_module"
hostmakedepends = ["python-setuptools","pkgconf"]
makedepends = [
  "dbus-devel",
  "fontconfig-devel",
  "freetype-devel",
  "go",
  "harfbuzz-devel",
  "lcms2-devel",
  "libcanberra-devel",
  "libpng-devel",
  "libxcursor-devel",
  "libxi-devel",
  "libxinerama-devel",
  "libxkbcommon-devel",
  "libxrandr-devel",
  "mesa-devel",
  "openssl-devel",
  "python-setuptools",
  "python-devel",
  "wayland-devel",
  "wayland-protocols",
  "xxhash-devel",
  "zlib-devel",
  "python-devel",
  "python-openssl"
]
checkdepends = ["python-pytest"]
depends = [ 
  "ncurses",
  "less",
  "python-pygments"
]
# a terminfo subpackage is needed if this is to be sent upstream
pkgdesc = "Modern, hackable, featureful, OpenGL based terminal emulator"
maintainer = "Mia <mia-rain@tuta.io>"
license = "GPL-3.0-only"
url = "https://sw.kovidgoyal.net/kitty"
source = f"https://github.com/kovidgoyal/kitty/archive/v{pkgver}.0.tar.gz"
sha256 = "d1fa72c9d16eedec43ba99de9f1ad511c8246cbe4e70dd1f9d865ef72984829d"

options = ["!check"]

tool_flags = {
  "LDFLAGS": [
    "-Wl",
    "-z",
    "stack-size=2097152"
    # See https://github.com/void-linux/void-packages/issues/7975
  ],
  "CFLAGS": [
    "-flto=auto",
    "-Wno-error=overflow"
  ]
}

def do_prepare(self):
    from cbuild.util import golang

    self.do("go", "mod", "vendor", allow_network=True)
    # golang.Golang(self).mod_download()
    # doesn't work here, idk why, not my problem tbh
 
def post_patch(self):
    self.rm("tools/utils/tpmfile_test.go")
    self.rm("kitty_tests/utmp.py")
    self.rm("kitty_tests/shell_integration.py")
    self.rm("kitty_tests/ssh.py")

def init_build(self):
    from cbuild.util import golang

    self.make_env.update(golang.get_go_env(self))

def do_build(self):
    self.do("python3", "./setup.py", "linux-package",
    '--disable-link-time-optimization',
    '--ignore-compiler-warnings',
    '--update-check-interval=0',
    "--verbose")
    self.mv("linux-package", "usr")

def do_install(self):
    self.install_files("usr", "./")