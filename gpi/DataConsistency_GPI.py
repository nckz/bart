# Copyright (c) 2014, Dignity Health
#
#     The GPI core node library is licensed under
# either the BSD 3-clause or the LGPL v. 3.
#
#     Under either license, the following additional term applies:
#
#         NO CLINICAL USE.  THE SOFTWARE IS NOT INTENDED FOR COMMERCIAL
# PURPOSES AND SHOULD BE USED ONLY FOR NON-COMMERCIAL RESEARCH PURPOSES.  THE
# SOFTWARE MAY NOT IN ANY EVENT BE USED FOR ANY CLINICAL OR DIAGNOSTIC
# PURPOSES.  YOU ACKNOWLEDGE AND AGREE THAT THE SOFTWARE IS NOT INTENDED FOR
# USE IN ANY HIGH RISK OR STRICT LIABILITY ACTIVITY, INCLUDING BUT NOT LIMITED
# TO LIFE SUPPORT OR EMERGENCY MEDICAL OPERATIONS OR USES.  LICENSOR MAKES NO
# WARRANTY AND HAS NOR LIABILITY ARISING FROM ANY USE OF THE SOFTWARE IN ANY
# HIGH RISK OR STRICT LIABILITY ACTIVITIES.
#
#     If you elect to license the GPI core node library under the LGPL the
# following applies:
#
#         This file is part of the GPI core node library.
#
#         The GPI core node library is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version. GPI core node library is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
#         You should have received a copy of the GNU Lesser General Public
# License along with the GPI core node library. If not, see
# <http://www.gnu.org/licenses/>.


# Author: Nick Zwart
# Date: 2015apr07
# Brief: A simple node to get things started.  Just copy this file to your
#        working directory, rename the 'NewNode' part, and start hacking. This
#        provides a push button widget, input and output array and info logger.

import gpi

import numpy as np


class ExternalNode(gpi.NodeAPI):
    '''
    '''

    def initUI(self):
        # Widgets

        # IO Ports
        self.addInPort('X_iter', 'NPYarray')
        self.addInPort('X_sampled', 'NPYarray')

        self.addOutPort('out', 'NPYarray')

    def compute(self):
        '''This is where the main algorithm should be implemented.
        '''

        Y = self.getData('X_sampled')
        X = self.getData('X_iter')


        X_hat = np.where(Y == 0 + 0j, X, Y)

        self.setData('out', X_hat)
        # GETTING WIDGET INFO

        # GETTING PORT DATA

        # SETTING PORT DATA


        return 0
