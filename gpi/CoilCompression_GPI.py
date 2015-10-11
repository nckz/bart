# GPI (v0.5.0-n1) auto-generated library file.
#
# FILE: /Users/nick/gpi/nick/default/GPI/MyNode_GPI.py
#
# For node API examples (i.e. widgets and ports) look at the
# core.interfaces.Template node.
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
    '''Usage: cc [-A] [-r cal_size] [-P num_coeffs] <kspace> <coeff>|<proj_kspace>
    
    Performs coil compression.
    
    -P N    perform compression to N virtual channels
    -r S    size of calibration region
    -A  use all data to compute coefficients
    -S|G|E  type: SVD, Geometric, ESPIRiT
    -h  help
    '''

    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'virtual channels', min=1, val=5)
        self.addWidget('SpinBox', 'calibration size', min=1, val=10)
        self.addWidget('PushButton', 'Use All Data', toggle=True)
        self.addWidget('ExclusivePushButtons', 'Compression Type:', buttons=['SVD', 'Geometric', 'ESPIRiT'], val=0)

        # IO Ports
        self.addInPort('kspace', 'NPYarray', obligation=gpi.REQUIRED)
        self.addInPort('coeff', 'NPYarray', obligation=gpi.REQUIRED)
        self.addOutPort('proj_kspace', 'NPYarray')

        return 0

    def compute(self):

        p = self.getVal('virtual channels')
        r = self.getVal('calibration size')
        a = self.getVal('Use All Data')
        comptype = self.getVal('Compression Type:')

        kspace = self.getData('kspace')
        coeff = self.getData('coeff')

        # load up arguments list
        args = [base_path+'/cc']
        args += ['-P '+str(p)]
        args += ['-r '+str(r)]
        if a:
            args += ['-A']

        if comptype == 0:
            args += ['-S']
        elif comptype == 1:
            args += ['-G']
        else:
            args += ['-E']

        # setup file for passing data to external command
        in1 = IFile(cfl.writecfl, kspace, asuffix=['.cfl','.hdr'])
        args += [in1]
        in2 = IFile(cfl.writecfl, coeff, asuffix=['.cfl','.hdr'])
        args += [in2]

        # setup file for getting data from external command
        out = OFile(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print(Command(*args))

        self.setData('proj_kspace', out.data())
        out.close()

        return 0
