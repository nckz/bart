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
    '''Usage: calmat [-k kernel_size] [-r cal_size] <kspace> <calibration matrix>
    
    Compute calibration matrix.
    
    -k ksize    kernel size
    -r cal_size Limits the size of the calibration region.
    '''

    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'kernel size', min=1, val=6)
        self.addWidget('SpinBox', 'calibration region size', min=1, val=20)

        # IO Ports
        self.addInPort('kspace', 'NPYarray', obligation=gpi.REQUIRED)
        self.addOutPort('output', 'NPYarray')

        return 0

    def compute(self):

        k = self.getVal('kernel size')
        r = self.getVal('calibration region size')

        kspace = self.getData('kspace')

        # load up arguments list
        args = [base_path+'/calmat']
        args += ['-r '+str(r)]
        args += ['-k '+str(k)]

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
