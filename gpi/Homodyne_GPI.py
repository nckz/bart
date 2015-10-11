# Author: Ashley Anderson III <aganders3@gmail.com>
# Date: 2015-10-10 21:13
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
    '''Usage: homodyne dim fraction <input> <output>

    Perform homodyne reconstruction along dimension dim.
    '''
    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'dim', min=0)
        self.addWidget('DoubleSpinBox', 'fraction', min=0.5, max=1.0,
                       decimals=3, singlestep=0.01)

        # IO Ports
        self.addInPort('kspace', 'NPYarray')

        self.addOutPort('out', 'NPYarray')

        return 0

    def compute(self):
        kspace = self.getData('kspace')

        # load up arguments list
        args = [base_path+'/homodyne']

        args += [str(self.getVal('dim'))]
        args += [str(self.getVal('fraction'))]

        # setup file for passing data to external command
        in1 = IFilePath(cfl.writecfl, kspace, asuffix=['.cfl','.hdr'])
        args += [in1]

        out1 = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out1]

        # run commandline
        print(Command(*args))

        self.setData('out', out1.data())

        in1.close()
        out1.close()

        return 0
