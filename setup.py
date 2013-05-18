#!/usr/bin/python
"""
desc: Setup script for 'superblue_ndvi' package.
auth: Craig Wm. Versek (https://github.com/cversek)
date: 5/11/2013
notes: Install with "python setup.py install".
"""
import platform, os, shutil

PACKAGE_METADATA = {
    'name'    : 'superblue_ndvi',
    'version' : 'dev',
    'author'  : "Craig Versek",
}
    
PACKAGE_SOURCE_DIR = 'src'
MAIN_PACKAGE_DIR = 'superblue_ndvi'
MAIN_PACKAGE_PATH = os.path.abspath(os.sep.join((PACKAGE_SOURCE_DIR,MAIN_PACKAGE_DIR)))

#scripts and plugins
ENTRY_POINTS = {
                 'console_scripts': [
                                      'superblue_user = superblue_ndvi.usercapture:main',
                                      'superblue_auto = superblue_ndvi.autocapture:main',
                                    ],
                } 

if __name__ == "__main__":
    from setuptools import setup, find_packages
    setup(package_dir = {'':PACKAGE_SOURCE_DIR},
          packages = find_packages(PACKAGE_SOURCE_DIR),
          
          #non-code files
          package_data = {'': ['*.so']},
          entry_points     = ENTRY_POINTS,
          **PACKAGE_METADATA
         )
