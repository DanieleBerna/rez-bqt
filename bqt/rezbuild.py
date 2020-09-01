  
"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
import sys
import zipfile
import fileinput
from shutil import copy


def build(source_path, build_path, install_path, targets):
    print("Running rezbuild.py...")

    if int(os.getenv("REZ_BUILD_INSTALL")):
        # This part is called with `rez build --install`
        payload_filename = os.environ["BQT_ARCHIVE"]
        with zipfile.ZipFile(os.path.join(source_path, "payload", payload_filename), 'r') as payload_archive:
            payload_archive.extractall(install_path)
            payload_archive.close()
        
        stylesheet_filepath = os.path.join(install_path, "bqt", "blender_stylesheet.qss")
        try:
            print(install_path)
            install_path = install_path.replace('\\','/')
            print(install_path)
            for line in fileinput.input(stylesheet_filepath, inplace=1):
                print(line.replace("../../startup", install_path ).rstrip())
        except IOError as e:
            print(f"Error while changing images path in stylesheet\n{e}")

        copy(os.path.join(source_path,"blender_addon_startup.py"),install_path)
            
if __name__ == '__main__':
    build(source_path=os.environ['REZ_BUILD_SOURCE_PATH'],
          build_path=os.environ['REZ_BUILD_PATH'],
          install_path=os.environ['REZ_BUILD_INSTALL_PATH'],
          targets=sys.argv[1:])