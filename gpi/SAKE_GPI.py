# GPI (v0.5.0-n1) auto-generated library file.
#
# FILE: /Users/nick/gpi/nick/default/GPI/MyNode_GPI.py
#
# For node API examples (i.e. widgets and ports) look at the
# core.interfaces.Template node.
from __future__ import absolute_import, division, print_function, unicode_literals

import os

# gpi, future
import gpi
from bart.gpi.borg import IFilePath, OFilePath, Command

# bart
import bart
base_path = bart.__path__[0] # library base for executables
import bart.python.cfl as cfl

class ExternalNode(gpi.NodeAPI):
    '''Usage: sake [-i iterations] [-s rel. subspace] <kspace> <output>
    
    Use SAKE algorithm to recover a full k-space from undersampled
    data using low-rank matrix completion.
    
    -i  number of iterations
    -s  rel. size of the signal subspace
    '''

    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'iterations', min=1, val=1)
        self.addWidget('SpinBox', 'relative subspace size', min=1, val=10)

        # IO Ports
        self.addInPort('kspace', 'NPYarray')
        self.addOutPort('output', 'NPYarray')

        return 0

    def compute(self):

        i = self.getVal('iterations')
        s = self.getVal('relative subspace size')

        kspace = self.getData('kspace')

        # load up arguments list
        args = [base_path+'/sake']
        args += [str(i)]
        args += [str(s)]

        # setup file for passing data to external command
        in1 = IFilePath(cfl.writecfl, kspace, asuffix=['.cfl','.hdr'])
        args += [in1]

        # setup file for getting data from external command
        out = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print(Command(*args))

        self.setData('output', out.data())
        out.close()

        return 0
