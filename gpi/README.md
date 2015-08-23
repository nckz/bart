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
