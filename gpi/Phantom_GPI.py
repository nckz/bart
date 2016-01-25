# Author: Ashley Anderson III <aganders3@gmail.com>
# Date: 2015-10-20 14:15
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
    """Usage: phantom [-k | -s nc] [-t trajectory] <output>

    Image and k-space domain phantoms.

    -s nc   nc sensitivities
    -k  k-space
    """

    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'num_coils', val=1, max=8)
        self.addWidget('PushButton', 'kspace', toggle=True)

        # IO Ports
        self.addInPort('traj', 'NPYarray', obligation=gpi.OPTIONAL)
        self.addOutPort('out1', 'NPYarray')

        return 0

    def compute(self):
        # load up arguments list
        args = [base_path+'/bart phantom']
        args += ['-s {}'.format(self.getVal('num_coils'))]

        if self.getVal('kspace'):
            args += ['-k']

        traj = self.getData('traj')
        if traj is not None:
            traj_file = IFilePath(cfl.writecfl, traj, asuffix=['.cfl', '.hdr'])
            args += ['-t', traj_file]

        # setup file for getting data from external command
        out = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
        args += [out]

        # run commandline
        print(Command(*args))

        self.setData('out1', out.data())
        out.close()

        return 0
