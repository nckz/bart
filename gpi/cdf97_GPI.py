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
    """Usage: cdf97 [-i] bitmask <input> <output>

    Perform a wavelet (cdf97) transform.

    -i  inverse
    -h  help
    """

    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'bitmask', val=3)
        self.addWidget('PushButton', 'compute', toggle=True)
        self.addWidget(
            'PushButton', 'direction', button_title='FORWARD', toggle=True)
        # IO Ports
        self.addInPort('input', 'NPYarray')
        self.addOutPort('output', 'NPYarray')

        return 0

    def validate(self):
        '''update the widget bounds based on the input data
        '''

        if 'direction' in self.widgetEvents():
            direction = self.getVal('direction')
            if direction:
                self.setAttr('direction', button_title="INVERSE")
            else:
                self.setAttr('direction', button_title="FORWARD")

        return 0


    def compute(self):

        if self.getVal('compute'):

            direction = self.getVal('direction')
            bm = self.getVal('bitmask')
            kspace = self.getData('input')

            # load up arguments list
            args = [base_path+'/bart cdf97']

            if direction != 0:
                args += ['-i']

            args += [str(bm)]

            in1 = IFilePath(cfl.writecfl, kspace, asuffix=['.cfl', '.hdr'])
            args += [in1]

            # setup file for getting data from external command
            out = OFilePath(cfl.readcfl, asuffix=['.cfl','.hdr'])
            args += [out]

            # run commandline
            print(Command(*args))

            self.setData('output', out.data())
            out.close()

        return 0

