from setuptools import setup
    
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="package-wizard",

    version="0.0.1",

    description="The Package-wizard is a PyQt5 package installer.",
    long_description = """
    The Package-wizard is a PyQt5 package installer.
    Project idea and design: Charles K. B.     
    Maintainer: Miklos Horvath 
    """,
    
    url="https://github.com/blackPantherOS/package-wizard",

    author="Charles Barcza, Miklos Horvath",
    maintainer="Miklos Horvath <hmiki@blackpantheros.eu>",
    
    license="GPLv3+",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",

        "Topic :: Desktop Environment",
        "Topic :: Desktop Environment :: K Desktop Environment (KDE)",
        "Topic :: System :: Software Distribution",
        "Environment :: X11 Applications :: Qt",
        
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: POSIX :: BSD :: OpenBSD",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],

    packages=["package_wizard"],
    
    scripts=["bin/package-wizard"],
    
    install_requires = ["argparse", "configparser"]
)
