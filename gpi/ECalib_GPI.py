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
    '''Usage: ./ecalib [-n num. s.values] [-t eigenv. threshold] [-c crop_value] [-k kernel_size] [-r cal_size] [-m maps] <kspace> <sensitivites> [<ev-maps>]
    
    Estimate coil sensitivities using ESPIRiT calibration.
    Optionally outputs the eigenvalue maps.
    
    -t threshold    This determined the size of the null-space.
    -c crop_value   Crop the sensitivities if the eigenvalue is smaller than {crop_value}.
    -k ksize    kernel size
    -r cal_size Limits the size of the calibration region.
    -m maps     Number of maps to compute.
    -I      intensity correction
    -1      perform only first part of the calibration
    '''

    def initUI(self):
        # Widgets
        self.addWidget('DoubleSpinBox', 'threshold', min=.01, val=1.0)
        self.addWidget('DoubleSpinBox', 'crop value', min=.01, val=1.0)
        self.addWidget('SpinBox', 'kernel size', min=1, val=5)
        self.addWidget('SpinBox', 'calibration size', min=1, val=20)
        self.addWidget('SpinBox', 'number maps', min=1, val=2)
        self.addWidget('PushButton', 'intensity correction', toggle=True)
        self.addWidget('PushButton', '1st part only', toggle=True)

        # IO Ports
        self.addInPort('kspace', 'NPYarray', obligation=gpi.REQUIRED)
        self.addOutPort('sensitivities', 'NPYarray')
        self.addOutPort('ev_maps', 'NPYarray')

        return 0

    def compute(self):

        t = self.getVal('threshold')
        c = self.getVal('crop value')
        k = self.getVal('kernel size')
        r = self.getVal('calibration size')
        m = self.getVal('number maps')
        I = self.getVal('intensity correction')
        first = self.getVal('1st part only')

        kspace = self.getData('kspace')

        # load up arguments list
        args = [base_path+'/ecalib']
        args += ['-t '+str(t)]
        args += ['-c '+str(c)]
        args += ['-k '+str(k)]
        args += ['-r '+str(r)]
        args += ['-m '+str(m)]
        if I:
            args += ['-I']
        if first:
            args += ['-1']

        # setup file for passing data to external command
        in1 = IFilePath(cfl.writecfl, kspace, asuffix=['.cfl','.hdr'])
        args += [in1]

        # setup file for getting data from external command
        out1 = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out1]
        out2 = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out2]

        # run commandline
        print(Command(*args))

        self.setData('sensitivities', out1.data())
        out1.close()
        self.setData('ev_maps', out2.data())
        out2.close()

        return 0
