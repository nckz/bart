# Author: Ashley Anderson III <aganders3@gmail.com>
# Date: 2015-10-10 19:37
# Copyright (C) 2015 Dignity Health

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
    '''Usage: poisson [-Y/Z dim] [-y/z acc] [-v] [-e] [-C center] <outfile>

    Computes Poisson-disc sampling pattern.

    -Y  size dimension 1 (phase 1)
    -Z  size dimension 2 (phase 2)
    -y  acceleration (dim 1)
    -z  acceleration (dim 2)
    -C  size of calibration region
    -v  variable density
    -e  elliptical scanning
    '''

    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'y size', min=3)
        self.addWidget('SpinBox', 'z size', min=3)
        self.addWidget('SpinBox', 'y accel', min=1, val=2)
        self.addWidget('SpinBox', 'z accel', min=1, val=2)
        self.addWidget('SpinBox', 'cal size', min=0, val=0)
        self.addWidget('PushButton', 'variable density', toggle=True)
        self.addWidget('PushButton', 'elliptical', toggle=True)

        # IO Ports
        self.addOutPort('out', 'NPYarray')

        return 0

    def validate(self):
        if (self.getVal('cal size') > self.getVal('y size')
         or self.getVal('cal size') > self.getVal('y size')):
            return -1

        return 0

    def compute(self):
        # load up arguments list
        args = [base_path+'/poisson']
        args += ['-Y {}'.format(self.getVal('y size'))]
        args += ['-Z {}'.format(self.getVal('z size'))]
        args += ['-y {}'.format(self.getVal('y accel'))]
        args += ['-z {}'.format(self.getVal('z accel'))]
        args += ['-C {}'.format(self.getVal('cal size'))]

        if self.getVal('variable density'):
            args += ['-v']

        if self.getVal('elliptical'):
            args += ['-e']

        # setup file for getting data from external command
        out = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print(Command(*args))

        self.setData('out', out.data())
        out.close()

        return 0
