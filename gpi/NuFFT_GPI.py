# Author: Nick Zwart
# Date: 2015-10-10
# Copyright (c) 2015 Dignity Health

from __future__ import absolute_import, division, print_function

import os, re

# gpi
import gpi
from bart.gpi.borg import IFilePath, OFilePath, Command

# bart
import bart
base_path = bart.__path__[0] # library base for executables
import bart.python.cfl as cfl

class ExternalNode(gpi.NodeAPI):
    '''Usage: ./nufft <traj> <input> <output>

        Perform non-uniform Fast Fourier Transform.

        -a      adjoint
        -i      inverse
        -d x:y:z        dimensions
        -t      toeplitz
        -l lambda       l2 regularization
        -h      help
    '''

    def initUI(self):
        # Widgets
        self.addWidget('PushButton', 'adjoint', toggle=True)
        self.addWidget('PushButton', 'inverse', toggle=True)
        self.addWidget('StringBox', 'dimensions', val='', placeholder='x:y:z')
        self.addWidget('PushButton', 'toeplitz', toggle=True)
        self.addWidget('DoubleSpinBox', 'lambda', min=0.0, val=0.0)

        # IO Ports
        self.addInPort('traj', 'NPYarray', obligation=gpi.REQUIRED, ndim=3)
        self.addInPort('input', 'NPYarray', obligation=gpi.REQUIRED)
        self.addOutPort('output', 'NPYarray')

        return 0

    def compute(self):

        adjoint = self.getVal('adjoint')
        inverse = self.getVal('inverse')
        dimensions = self.getVal('dimensions')
        toeplitz = self.getVal('toeplitz')
        lmbda = self.getVal('lambda')

        kspace = self.getData('input')
        traj = self.getData('traj')

        # load up arguments list
        args = [base_path+'/bart nufft']

        args += ['-l '+str(lmbda)]
        if adjoint:
            args += ['-a']
        if inverse:
            args += ['-i']
        if toeplitz:
            args += ['-t']
        if dimensions != '':
            try:
                dims = re.search('^([0-9]*):([0-9]*):([0-9]*)$', dimensions).groups()
                args += ['-d '+':'.join(dims)]
            except:
                self.log.warn('\'dimensions\' must be a list of positive integers delimited by colons (i.e. int:int:int), skipping...')

        # setup file for passing data to external command
        in_traj = IFilePath(cfl.writecfl, traj, asuffix=['.cfl','.hdr'])
        in_kspc = IFilePath(cfl.writecfl, kspace, asuffix=['.cfl','.hdr'])
        args += [in_traj, in_kspc]

        # setup file for getting data from external command
        out = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print(Command(*args))

        self.setData('output', out.data())
        out.close()
        in_traj.close()
        in_kspc.close()

        return 0
