# GPI-BART Nodes
This directory contains node wrappers for the BART toolbox binaries. This patch
turns the base BART directory into a python library with 'gpi' and 'python'
sub-libraries.  To install this as a GPI node-library, clone the repository
from github as 'bart' in your local GPI node directory:

    $ mkdir ~/gpi
    $ cd ~/gpi
    $ git clone https://github.com/nckz/bart.git bart

Then follow the instructions for installing dependencies and making the BART
toolbox for your platform.

    $ less ~/gpi/bart/README

# Examples
The [example1_espirit_recon_py2_GPI.net](https://github.com/nckz/bart/blob/master/gpi/example1_espirit_recon_py2_GPI.net) is a GPI network that matches the example #1 in the bart example script [here](http://mikgroup.github.io/bart/examples.html).
The data for this network can be found [here](https://github.com/mikgroup/espirit-matlab-examples/tree/master/data).
This example makes use of the *und2x2* and *full* datasets.
