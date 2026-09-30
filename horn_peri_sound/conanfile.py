from pathlib import Path

from conan import ConanFile
from conan.tools.files import copy


class FunctionalTestConan(ConanFile):
    name = "veds-rh850-mbd-functional-test"

    settings = "build_type"

    requires = "fnv4-veds/[>=5.1.2]"

    def generate(self):
        veds = self.dependencies["fnv4-veds"]
        copy(self, "*", veds.cpp_info.bindir, self.build_folder)
        for req, dep in self.dependencies.items():
            dep_build_folder = Path(self.build_folder) / "upstream" / req.ref.name
            for srcdir in dep.cpp_info.srcdirs:
                copy(self, "*", srcdir, dep_build_folder / "src")
            for incldir in dep.cpp_info.includedirs:
                copy(self, "*", incldir, dep_build_folder / "include")

    def layout(self):
        self.folders.root = self.recipe_folder
        self.folders.build = Path("build") / str(self.settings.build_type)
        self.folders.generators = self.folders.build / "generators"
