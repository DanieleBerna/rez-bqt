  
"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os

name = 'bqt'

requires = [
    'PySide2',
    'pypiwin32'
]

_BQT_VERSION_ENV_KEY = "BQT_RESOLVED_BUILD_VERSION"
_PAYLOAD_FILENAME_BASE = "bqt_"

@early()
def version():
    """
    This function searchs for a bqt_version.zip file and return version number
    :return: the version string
    """
    # If we've already run this, then don't run it again
    bqt_ver = os.getenv(_BQT_VERSION_ENV_KEY)
    if bqt_ver:
        return bqt_ver
        
    print("Getting bqt version from zip")
    
    this_dir = os.getcwd() # Rez execs this file so there's no reference to this directory at this time.
    payload_dir = os.path.join(this_dir, 'payload') # Find the payload folder contining the zip

    
    # Make sure the necessary directories exist
    if not os.path.exists(payload_dir):
        raise IOError(f"Failed to find: {payload_dir}")
        
    # Make sure the bqt zip file exists
    payloads = [p for p in os.listdir(payload_dir) if p.lower().find(_PAYLOAD_FILENAME_BASE) != -1]
    if not payloads:
        raise IOError("Failed to find bqt.zip payload")
        
    archive_filename = os.path.join(payload_dir, payloads[0])
    ver = payloads[0].split(_PAYLOAD_FILENAME)[1][:-4]
    os.environ["BQT_ARCHIVE"] = archive_filename
    
    # Add a suffix if provided
    import sys
    if '--suffix' in sys.argv:
        idx = sys.argv.index('--suffix')
        ver += ".{}".format(sys.argv[idx+1])
    
    # Cache this value in the environment variables so we don't run this all over again unnecesarily 
    os.environ[_BQT_VERSION_ENV_KEY] = ver
    return ver
    
def commands():
    env['PYTHONPATH'].append('{root}')
    env['REZ_bqt_STARTUP'].append('{root}/bqt_addon_startup.py')

build_command = "T:/ugcore/rez/Scripts/python {root}/rezbuild.py"
