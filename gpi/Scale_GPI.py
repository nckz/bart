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
        self.addWidget('DoubleSpinBox', 'factor', min=0.01, val=1.0)

        # IO Ports
        self.addInPort('in', 'NPYarray')
        self.addOutPort('out', 'NPYarray')

        return 0

    def compute(self):

        f = self.getVal('factor')
        indata = self.getData('in')

        # load up arguments list
        args = [base_path+'/scale']
        args += [str(f)]

        # setup file for passing data to external command
        inp = IFile(cfl.writecfl, indata, asuffix=['.cfl','.hdr'])
        args += [inp]

        # setup file for getting data from external command
        out = OFile(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print((Command(args)))

        self.setData('out', out.data())
        out.close()
        inp.close()

        return 0
