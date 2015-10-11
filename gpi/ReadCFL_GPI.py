# Author: Nick Zwart
# Date: 2015-10-10
# Copyright (c) 2015 Dignity Health

from __future__ import absolute_import, division, print_function

import os
import time
import gpi
import numpy as np

# bart
import bart
import bart.python.cfl as cfl

class ExternalNode(gpi.NodeAPI):
    """Read arrays that were written as cfl+hdr files
    
    OUTPUT: Numpy array read from file

    WIDGETS:
    I/O Info - Gives info on data file and data type
    File Browser - button to launch file browser, and typein widget if the pathway is known.
    Squeeze - option for squeezing data, which removes all dimensions of length 1 (all data preserved)
    """

    def execType(self):
        # default executable type
        return gpi.GPI_THREAD
        # return gpi.GPI_PROCESS # this is the safest
        # return gpi.GPI_APPLOOP

    def initUI(self):

       # Widgets
        self.addWidget('TextBox', 'I/O Info:')
        self.addWidget('OpenFileBrowser', 'File Browser',
                button_title='Browse', caption='Open File', filter='complex float (*.cfl)')
        self.addWidget('PushButton', 'Squeeze', toggle=True)

        # IO Ports
        self.addOutPort(title='out', type='NPYarray', dtype=np.complex64)

    def compute(self):

        import os
        import time
        import numpy as np

        # start file browser
        fname = gpi.TranslateFileURI(self.getVal('File Browser'))

        # check that the path actually exists
        if not os.path.exists(fname):
            self.log.node("Path does not exist: "+str(fname))
            return 0

        # show some file stats
        fstats = os.stat(fname)
        # creation
        ctime = time.strftime('%d/%m/20%y', time.localtime(fstats.st_ctime))
        # mod time
        mtime = time.strftime('%d/%m/20%y', time.localtime(fstats.st_mtime))
        # access time
        atime = time.strftime('%d/%m/20%y', time.localtime(fstats.st_atime))
        # filesize
        fsize = fstats.st_size
        # user id
        uid = fstats.st_uid
        # group id
        gid = fstats.st_gid

        # read the data
        # takes the base filename
        fname = os.path.splitext(fname)[0]
        out = cfl.readcfl(fname) 

        if self.getVal('Squeeze'):
            out = out.squeeze()

        d1 = list(out.shape)
        info = "created: "+str(ctime)+"\n" \
               "accessed: "+str(atime)+"\n" \
               "modified: "+str(mtime)+"\n" \
               "UID: "+str(uid)+"\n" \
               "GID: "+str(gid)+"\n" \
               "file size (bytes): "+str(fsize)+"\n" \
               "dimensions: "+str(d1)+"\n" \
               "type: "+str(out.dtype)+"\n"
        self.setAttr('I/O Info:', val=info)

        self.setData('out', out)

        return(0)
