# GPI (v0.5.0-n1) auto-generated library file.
#
# FILE: /Users/nick/gpi/nick/default/GPI/MyNode_GPI.py
#
# For node API examples (i.e. widgets and ports) look at the
# core.interfaces.Template node.

import os

# gpi, future
import gpi
from bart.python.ebe import IFile, OFile, Command

# bart
import bart
base_path = bart.__path__[0] # library base for executables
import bart.python.cfl as cfl

class ExternalNode(gpi.NodeAPI):
    '''About text goes here...
    '''

    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'readout samples', min=128)
        self.addWidget('SpinBox', 'phase encoding lines', min=128)
        self.addWidget('SpinBox', 'acceleration', min=1)
        self.addWidget('PushButton', 'radial', toggle=True)
        self.addWidget('PushButton', 'golden angle', toggle=True)

        # IO Ports
        self.addOutPort('out1', 'NPYarray')

        return 0

    def compute(self):

        x = self.getVal('readout samples')
        y = self.getVal('phase encoding lines')
        a = self.getVal('acceleration')
        r = self.getVal('radial')
        g = self.getVal('golden angle')

        # load up arguments list
        args = [base_path+'/traj']
        args += ['-x '+str(x)]
        args += ['-y '+str(y)]
        args += ['-a '+str(a)]
        if r:
            args += ['-r']
        if g:
            args += ['-G']

        # set output filename
        out = OFile(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print Command(args)

        self.setData('out1', out.data())
        out.close()

        return 0
