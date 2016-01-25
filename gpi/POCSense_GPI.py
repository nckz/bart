# Author: Ryan Robison
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
    '''Usage: pocsense [-l1/-l2] [-r lambda] <kspace> <sensitivities> <output>

    Perform POCSENSE reconstruction.
    -l1/-l2 toggle l1-wavelet or l2 regularization.
    -r alpha    regularization parameter
    '''

    def initUI(self):
        # Widgets
        self.addWidget('ExclusivePushButtons', 'Regularization:', buttons=['l1-wavelet', 'l2'], val=0)
        self.addWidget('DoubleSpinBox', 'regularization parameter', val=0.0, decimals=5)

        # IO Ports
        self.addInPort('kspace', 'NPYarray', obligation=gpi.REQUIRED)
        self.addInPort('sensitivities', 'NPYarray', obligation=gpi.REQUIRED)
        self.addOutPort('output', 'NPYarray')

        return 0

    def compute(self):

        reg = self.getVal('Regularization:')
        alpha = self.getVal('regularization parameter')
        kspace = self.getData('kspace')
        inmaps = self.getData('sensitivities')

        # load up arguments list
        args = [base_path+'/bart pocsense']
        if reg == 0:
            args += ['-l1']
        else:
            args += ['-l2']
        args += ['-r '+str(alpha)]

        # setup file for passing data to external command
        coords = IFilePath(cfl.writecfl, kspace, asuffix=['.cfl','.hdr'])
        args += [coords]
        sens = IFilePath(cfl.writecfl, inmaps, asuffix=['.cfl','.hdr'])
        args += [sens]

        # setup file for getting data from external command
        out = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print(Command(*args))

        self.setData('output', out.data())
        out.close()

        return 0
