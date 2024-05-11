import os

from conan import ConanFile
from conan.tools.files import copy
from conan.tools.env import Environment

class QBittorrentConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ["CMakeDeps"]

    requires = [
        "libtorrent/2.0.10",
        "openssl/3.2.1",
        "boost/1.81.0",
        "zlib/1.2.11",
        "qt/6.5.0"
    ]

    default_options = {
        "qt/*:shared": True,
        "qt/*:qttools": True,
        "qt/*:qtsvg": True,
    }

    def generate(self):
        env = Environment()
        env.define('CMAKE_PREFIX_PATH', self.dependencies['qt'].package_folder + "/lib/cmake")

        for dep in self.dependencies.values():
            if (dep == self.dependencies['qt']):
                plugins = os.path.join(self.dependencies['qt'].package_folder, "res", "archdatadir", "plugins")
                dest = os.path.join(self.build_folder)
                dll_wild_card = "*.dll"
                copy(self, dll_wild_card, plugins, dest)
                copy(self, dll_wild_card, dep.cpp_info.bindir, self.build_folder)
