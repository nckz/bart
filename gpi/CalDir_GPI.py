# Author: Nick Zwart
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
    '''Usage: ./caldir cal_size <input> <output>

        Estimates coil sensitivities from the k-space center using
        a direct method (McKenzie et al.). The size of the fully-sampled
        calibration region is automatically determined but limited by
        {cal_size} (e.g. in the readout direction).
    '''

    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'calibration region size', min=1, val=20)

        # IO Ports
        self.addInPort('input', 'NPYarray', obligation=gpi.REQUIRED)
        self.addOutPort('output', 'NPYarray')

        return 0

    def compute(self):

        r = self.getVal('calibration region size')
        kspace = self.getData('input')

        # load up arguments list
        args = [base_path+'/bart caldir']
        args += [str(r)]

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
