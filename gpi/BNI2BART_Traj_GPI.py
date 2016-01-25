# Author: Ashley Anderson III <aganders3@gmail.com>
# Date: 2016-01-25 13:58

import numpy as np
import gpi

class ExternalNode(gpi.NodeAPI):
    """Transform coordinates from BNI conventions to BART conventions.

    INPUT:
        in - a numpy arrary of k-space coordinates in the BNI convention
            i.e. (-0.5, 0.5), dimensions: [readouts, pts, xy(z)]
    OUTPUT:
        out - a numpy array of k-space coordinates in the BART convention
            i.e. (-mtx/2, mtx/2), dimensions: [zyx, pts, readouts]
    WIDGETS:
        mtx - the resulting matrix size (assumed square/cubic)
    """

    # initialize the UI - add widgets and input/output ports
    def initUI(self):
        # Widgets
        self.addWidget('SpinBox', 'mtx', val=128, min=1, max=1024)
        # self.addWidget('DoubleSpinBox', 'bar', val=10, min=0, max=100)
        # self.addWidget('PushButton', 'baz', toggle=True)
        # self.addWidget('ExclusivePushButtons', 'qux',
        #              buttons=['Antoine', 'Colby', 'Trotter', 'Adair'], val=1)

        # IO Ports
        self.addInPort('in', 'NPYarray', ndim=3)
        self.addOutPort('out', 'NPYarray', dtype=np.complex64, ndim=3)


    # validate the data - runs immediately before compute
    # your last chance to show/hide/edit widgets
    # return 1 if the data is not valid - compute will not run
    # return 0 if the data is valid - compute will run
    def validate(self):
        in_data = self.getData('in')

        # TODO: make sure the input data is valid
        # [your code here]

        return 0

    # process the input data, send it to the output port
    # return 1 if the computation failed
    # return 0 if the computation was successful
    def compute(self):
        coords = self.getData('in').copy()
        mtx = self.getVal('mtx')

        # just transpose first to reverse dimensions
        coords = coords.T

        # adjust by the matrix size
        # TODO: account for "true resolution"
        coords *= mtx

        # reverse the xyz dimension
        coords[:,...] = coords[::-1,...]

        # pad the z-dimension with zeros if the trajectory is 2D
        if coords.shape[0] == 2:
            coords = np.pad(coords,
                            ((0,1), (0,0), (0,0)),
                            mode='constant',
                            constant_values=0)

        # if the trajectory is not 3D at this point, something has gone wrong
        if coords.shape[0] != 3:
            self.log.warn("The final dimensions of the input data must be 2 (xy), or 3 (xyz).")
            return 1

        self.setData('out', np.require(coords, dtype=np.complex64))

        return 0
