from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        "database",
        ["database.cpp"],
        include_dirs=["..\\lib"],
        library_dirs=["..\\lib"],
        libraries=["sqlite3"],
    ),
]

setup(
    name="database",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
