# Copyright (c) 2014, Dignity Health
#
# Author: Ashley Anderson III <aganders3@gmail.com>
# Date: 2016-01-25 09:50

import gpi
import numpy as np
import bart.python.cfl as cfl
import os

class ExternalNode(gpi.NodeAPI):
    """Uses the numpy save interface for writing arrays.

    INPUT - numpy array to write

    WIDGETS:
    File Browser - button to launch file browser, and typein widget, to give pathname for output file
    Write Mode - write at any event, or write only with new filename
    Write Now - write right now
    """

    def initUI(self):

       # Widgets
        self.addWidget(
            'SaveFileBrowser', 'File Browser', button_title='Browse',
            caption='Save File (*.npy)', filter='cfl (*.cfl)')
        self.addWidget('PushButton', 'Write Mode', button_title='Write on New Filename', toggle=True)
        self.addWidget('PushButton', 'Write Now', button_title='Write Right Now', toggle=False)

        # IO Ports
        self.addInPort('in', 'NPYarray', dtype=np.complex64)

        # store for later use
        self.URI = gpi.TranslateFileURI

    def validate(self):

        if self.getVal('Write Mode'):
            self.setAttr('Write Mode', button_title="Write on Every Event")
        else:
            self.setAttr('Write Mode', button_title="Write on New Filename")

        fname = self.URI(self.getVal('File Browser'))
        self.setDetailLabel(fname)

        return 0

    def compute(self):

        if self.getVal('Write Mode') or self.getVal('Write Now') or ('File Browser' in self.widgetEvents()):

            fpath = self.URI(self.getVal('File Browser'))
            basedir, fname = os.path.split(fpath)
            basename, ext = os.path.splitext(fname)

            outpath = os.path.join(basedir, basename)

            data = self.getData('in')
            cfl.writecfl(outpath, data)

        return(0)
