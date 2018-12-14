#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

from TSVRESTTools.common import create_rest_app, create_cli_app

# BEGIN Add personality...
from config import dummy_tagger

command, tagger, args, kwargs = dummy_tagger
prog = tagger(*args, **kwargs)

# END Add personality...

# Create app with the desired parameters...
app = create_rest_app(__name__, command=command, internal_app=prog)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--pipe':  # TODO: It just a tech preview, implement it properly!
        create_cli_app(prog, sys.stdin, sys.stdout)
    else:
        app.run(debug=True)
