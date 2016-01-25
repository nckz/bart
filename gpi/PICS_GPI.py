# Author: Ashley Anderson III <aganders3@gmail.com>
# Date: 2015-10-10 16:14
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
    '''Usage: pics [-l1/-l2] [-r lambda] [-t <trajectory>] <kspace> <coil_maps> <output>

    Parallel-imaging compressed-sensing reconstruction.

    -l1/-l2     toggle l1-wavelet or l2 regularization.
    -r lambda   regularization parameter
    -c      real-value constraint
    -s step     iteration stepsize
    -i maxiter  number of iterations
    -t trajectory   k-space trajectory

    Generalized regularization options (experimental)
    -R <T>:A:B:C    <T> is regularization type (single letter),
        A is transform flags, B is joint threshold flags, and C is
        regularization value. Specify any number of regularization terms.
        -R Q:C      l2-norm in image domain
        -R I:B:C    l1-norm in image domain
        -R W:A:B:C  l1-wavelet
        -R T:A:B:C  total variation
        Example:
        -R T:7:0:.01    3D isotropic total variation with 0.01 regularization.
    '''

    def initUI(self):
        # Widgets
        self.addWidget('ExclusivePushButtons', 'regularization', buttons=('l1-wavelet', 'l2'), val=0)
        self.addWidget('DoubleSpinBox', 'lamb', val=0.01, min=0, max=1, decimals=5)

        # IO Ports
        self.addInPort('kspace', 'NPYarray')
        self.addInPort('coil_maps', 'NPYarray')
        self.addInPort('traj', 'NPYarray', obligation=gpi.OPTIONAL)

        self.addOutPort('output', 'NPYarray')

        return 0

    def compute(self):

        kspace = self.getData('kspace')
        coil_maps = self.getData('coil_maps')
        trajectory = self.getData('traj')

        reg = self.getVal('regularization')
        lamb = self.getVal('lamb')

        # load up arguments list
        args = [base_path+'/bart pics']

        if reg == 0:
            args += ['-l1']
        else:
            args += ['-l2']

        args += ['-r {}'.format(lamb)]
        args += ['-e -i 100']

        # setup file for getting data from external command
        if trajectory is not None:
            traj = IFilePath(cfl.writecfl, trajectory, asuffix=['.cfl','.hdr'])
            args += ['-t', traj]

        kspace = IFilePath(cfl.writecfl, kspace, asuffix=['.cfl','.hdr'])
        coil_maps = IFilePath(cfl.writecfl, coil_maps, asuffix=['.cfl','.hdr'])
        output = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [kspace, coil_maps, output]

        print(Command(*args))

        self.setData('output', output.data())

        if trajectory is not None:
            traj.close()
        kspace.close()
        coil_maps.close()
        output.close()

        return 0
