#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys

from TSVRESTTools.common import create_rest_app, create_cli_app

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'emmorphpy'))  # Needed to be able to use git submodule...
from emmorphpy import EmMorphPy

# Initialize tagger as wanted...
prog = EmMorphPy()

# TODO: Bálint: command should be the usual names e.g. /emMorph, /emDep, etc.
# Create app with the desired parameters...
app = create_rest_app(__name__, command='/emMorph', internal_app=prog)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--pipe':  # TODO: It just a tech preview, implement it properly!
        create_cli_app(prog, sys.stdin, sys.stdout)
    else:
        app.run(debug=True)
