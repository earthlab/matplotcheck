import os
from os import path
from numpy.distutils.core import setup


DISTNAME = "matplotcheck"
DESCRIPTION = "Functions to check Matplotlib plot outputs"
MAINTAINER = "Leah Wasser"
MAINTAINER_EMAIL = "leah.wasser@colorado.edu"
VERSION = "0.0.1"
DESCRIPTION = (
    "Functions to check and validate elements in a matplotlib created python plot."
)

def configuration(parent_package="", top_path=None):
    if os.path.exists("MANIFEST"):
        os.remove("MANIFEST")

    from numpy.distutils.misc_util import Configuration

    config = Configuration(None, parent_package, top_path)
    config.add_subpackage("matplotcheck")

    return config


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

if __name__ == "__main__":
    setup(
        configuration=configuration,
        name=DISTNAME,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        version=VERSION,
        install_requires=[
            "tqdm",
            "pandas",
            "numpy",
            "folium",
            "geopandas",
            "matplotlib",
            "rasterio",
            "python-dateutil",
            "scipy",
        ],
        zip_safe=False,  # the package can run out of an .egg file
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
        ],
    )
