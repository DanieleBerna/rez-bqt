  
"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

# Startup file for Blender. Executed when Blender starts in order to register the addon

import bqt
try:
    bqt.unregister()
except:
    pass
    
bqt.register()
bqt.instantiate_application()
