#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys

from TSVRESTTools.common import create_rest_app, create_cli_app

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'HunTag3'))
from huntag.tagger import Tagger
from huntag.transmodel import TransModel
from huntag.tools import get_featureset_yaml, data_sizes

# TODO: Bálint: legyen a neve emSeqTag
# Initialize tagger as wanted...
model_name = os.path.join(os.path.dirname(__file__), 'models', 'emChunk', 'testNP')
cfg_file = 'HunTag3/configs/maxnp.szeged.hfst.yaml'
tag_field = 'NP-BIO'

options = {'model_filename': '{0}{1}'.format(model_name, '.model'),
           'featcounter_filename': '{0}{1}'.format(model_name, '.featureNumbers.gz'),
           'labelcounter_filename': '{0}{1}'.format(model_name, '.labelNumbers.gz'),
           'tag_field': tag_field,
           'data_sizes': data_sizes
           }

print('loading transition model...', end='', file=sys.stderr, flush=True)
trans_model = TransModel.load_from_file('{0}{1}'.format(model_name, '.transmodel'))
print('done', file=sys.stderr, flush=True)

prog = Tagger(get_featureset_yaml(cfg_file), trans_model, options)

# END tagger initialisation...

# TODO: Bálint: command should be the usual names e.g. /emMorph, /emDep, etc.
# Create app with the desired parameters...
app = create_rest_app(__name__, command='/emChunk', internal_app=prog)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--pipe':  # TODO: It just a tech preview, implement it properly!
        create_cli_app(prog, sys.stdin, sys.stdout)
    else:
        app.run(debug=True)
