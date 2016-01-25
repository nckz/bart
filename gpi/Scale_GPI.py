# Author: Nick Zwart
# Date: 2015-10-10
# Copyright (c) 2015 Dignity Health

from __future__ import absolute_import, division, print_function

import os

# gpi, future
import gpi
from bart.gpi.borg import IFilePath, OFilePath, Command

# bart
import bart
base_path = bart.__path__[0] # library base for executables
import bart.python.cfl as cfl

class ExternalNode(gpi.NodeAPI):
    '''Usage: scale factor <input> <output>

    Scale array by {factor}. The scale factor can be a complex number.
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
        args = [base_path+'/bart scale']
        args += [str(f)]

        # setup file for passing data to external command
        inp = IFilePath(cfl.writecfl, indata, asuffix=['.cfl','.hdr'])
        args += [inp]

        # setup file for getting data from external command
        out = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print(Command(*args))

        self.setData('out', out.data())
        out.close()
        inp.close()

        return 0
