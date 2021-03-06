# Author: Ryan Robison
# Date: 2015-10-10
# Copyright (c) 2015 Dignity Health

from __future__ import absolute_import, division, print_function

import os

# gpi
import gpi
from bart.gpi.borg import IFilePath, OFilePath, Command

# bart
import bart
base_path = bart.__path__[0] # library base for executables
import bart.python.cfl as cfl

class ExternalNode(gpi.NodeAPI):
    '''Usage: threshold [-j bitmask] lambda <input> <output>

    Perform softthresholding with parameter lambda.

    -j bitmask  joint thresholding
    '''

    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'thresholding bitmask', min=0, val=0)
        self.addWidget('DoubleSpinBox', 'lambda', min=0, val=0.01, decimals=5)

        # IO Ports
        self.addInPort('input', 'NPYarray')
        self.addOutPort('output', 'NPYarray')

        return 0

    def compute(self):

        j = self.getVal('thresholding bitmask')
        lamda = self.getVal('lambda')

        inp = self.getData('input')

        # load up arguments list
        args = [base_path+'/bart threshold']
        args += ['-j '+str(j)]
        args += [str(lamda)]

        # setup file for passing data to external command
        in1 = IFilePath(cfl.writecfl, inp, asuffix=['.cfl','.hdr'])
        args += [in1]

        # setup file for getting data from external command
        out = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print(Command(*args))

        self.setData('output', out.data())
        out.close()

        return 0
