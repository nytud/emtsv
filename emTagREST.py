#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys

from TSVRESTTools.common import create_app

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'purepospy'))  # Needed to be able to use git submodule...
from purepospy import PurePOS

# Initialize tagger as wanted...
em_tag = PurePOS('models/emTag/test.purepos.model')

# TODO: Bálint: command should be the usual names e.g. /emMorph, /emDep, etc.
# Create app with the desired parameters...
app = create_app(__name__, command='/emTag', internal_app=em_tag)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--pipe':  # TODO: It just a tech preview, implement it properly!
        from TSVRESTTools.tsvhandler import process
        sys.stdout.writelines(process(sys.stdin, em_tag))
    else:
        app.run(debug=True)
