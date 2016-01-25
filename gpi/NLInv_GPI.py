# Author: Ashley Anderson III <aganders3@gmail.com>
# Date: 2015-10-10 19:59
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
    '''Usage: nlinv [-l1/-l2] [-i iterations] <kspace> <output> [<sensitivities>]

    Jointly estimate image and sensitivities with nonlinear
    inversion using {iter} iteration steps. Optionally outputs
    the sensitivities.
    '''

    def initUI(self):
        # Widgets
        self.addWidget('ExclusivePushButtons', 'regularization', buttons=('l1-wavelet', 'l2'), val=0)

        self.addWidget('SpinBox', 'iterations', min=1)

        # IO Ports
        self.addInPort('kspace', 'NPYarray', obligation=gpi.REQUIRED)

        self.addOutPort('out', 'NPYarray')
        self.addOutPort('sensitivities', 'NPYarray')

        return 0

    def compute(self):
        kspace = self.getData('kspace')

        # load up arguments list
        args = [base_path+'/bart nlinv']

        if self.getVal('regularization') == 0:
            args += ['-l1']
        else:
            args += ['-l2']

        args += ['-i {}'.format(self.getVal('iterations'))]

        # setup file for passing data to external command
        in1 = IFilePath(cfl.writecfl, kspace, asuffix=['.cfl','.hdr'])
        args += [in1]

        out1 = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out1]
        out2 = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out2]

        # run commandline
        print(Command(*args))

        self.setData('out', out1.data())
        self.setData('sensitivities', out2.data())

        in1.close()
        out1.close()
        out2.close()

        return 0
