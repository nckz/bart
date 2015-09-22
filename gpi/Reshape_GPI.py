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
        self.addWidget('StringBox', 'flags (bitmask)', val='2 10')
        self.addWidget('StringBox', 'dim1 ... dimN', val='21 1')

        #self.MAX_DIMS = 5
        #for i in xrange(1, self.MAX_DIMS+1):
        #    self.addWidget('SpinBox', 'dim'+str(i), min=1, val=1)

        # IO Ports
        self.addInPort('in', 'NPYarray')
        self.addOutPort('out', 'NPYarray')

        return 0

    def compute(self):

        flag = self.getVal('flags (bitmask)')
        #dims = [ str(self.getVal('dim'+str(i))) for i in xrange(1, self.MAX_DIMS+1) ]
        dims = self.getVal('dim1 ... dimN')

        indata = self.getData('in')

        # load up arguments list
        args = [base_path+'/reshape']
        args += ['$('+base_path+'/bitmask '+flag+')']
        args += [dims]

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

        return 0
