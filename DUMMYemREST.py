#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys

from TSVRESTTools.common import create_app

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'Dummy'))  # Needed to be able to use git submodule...
from DummyTagger.dummy import DummyTagger

# Initialize tagger as wanted...
dt = DummyTagger()

# TODO: Bálint: command should be the usual names e.g. /emMorph, /emDep, etc.
# Create app with the desired parameters...
app = create_app(__name__, command='/emTag', internal_app=dt)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--pipe':  # TODO: It just a tech preview, implement it properly!
        from TSVRESTTools.tsvhandler import process
        sys.stdout.writelines(process(sys.stdin, dt))
    app.run(debug=True)
