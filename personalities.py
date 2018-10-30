#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys

# DummyTagger (EXAMPLE)

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'Dummy'))  # Needed to be able to use git submodule...
from DummyTagger.dummy import DummyTagger

# Setup the triplet: command, class, args (tuple), kwargs (dict)
dummy_tagger = ('/dummy_tagger', DummyTagger, ('Params goes here', {'Source field names'}, ['Target field names']), {})


# emMorph

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'emmorphpy'))  # Needed to be able to use git submodule...
from emmorphpy import EmMorphPy

# TODO: Bálint: command should be the usual names e.g. /emMorph, /emDep, etc.
em_morph = ('/emMorph', EmMorphPy, (), {'source_fields': {'string'}, 'target_fields': ['anas']})

# emTag

sys.path.append(os.path.join(os.path.dirname(__file__), 'purepospy'))  # Needed to be able to use git submodule...
from purepospy import PurePOS

model_name = 'models/emTag/test.purepos.model'

em_tag = ('/emTag', PurePOS, (model_name,), {'source_fields': {'string', 'anas'},
                                             'target_fields': ['lemma', 'hfstana']})

# emDepTool

sys.path.append(os.path.join(os.path.dirname(__file__), 'deptoolpy'))  # Needed to be able to use git submodule...
from deptoolpy.deptoolpy import DepToolPy


em_deptool = ('/emDepTool', DepToolPy, ({'string', 'lemma', 'hfstana'}, ['pos', 'feature']), {})

# emChunk

sys.path.append(os.path.join(os.path.dirname(__file__), 'HunTag3'))
from huntag.tagger import Tagger
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
           'data_sizes': data_sizes,
           'transmodel_filename': '{0}{1}'.format(model_name, '.transmodel'),
           'target_fields': ['NP_BIO']
           }

features = get_featureset_yaml(cfg_file)

# TODO: Bálint: command should be the usual names e.g. /emMorph, /emDep, etc.
em_chunk = ('/emChunk', Tagger, (features, options), {})

# emDep

sys.path.append(os.path.join(os.path.dirname(__file__), 'emdeppy'))  # Needed to be able to use git submodule...
from emdeppy import EmDepPy

em_dep = ('/emDep', EmDepPy, ({'string', 'lemma', 'pos', 'feature'}, ['tokid', 'deptype', 'deptarget']), {})
