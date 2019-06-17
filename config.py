#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys
from collections import defaultdict

from __init__ import jnius_config

# DummyTagger (EXAMPLE) ################################################################################################

# Import Tagger class, and parameters...
from emdummy.dummytagger.dummytagger import DummyTagger

# Setup the triplet: class, args (tuple), kwargs (dict)
em_dummy = (DummyTagger, ('Params', 'goes', 'here'),
            {'source_fields': {'Source field names'}, 'target_fields': ['Target field names']})

# emToken ##############################################################################################################

from emtokenpy.emtokenpy import EmTokenPy

em_token = (EmTokenPy, (), {'source_fields': set(), 'target_fields': ['form']})

# emMorph ##############################################################################################################

from emmorphpy.emmorphpy import EmMorphPy

em_morph = (EmMorphPy, (), {'source_fields': {'form'}, 'target_fields': ['anas']})

# emTag ################################################################################################################

from purepospy.purepospy import PurePOS
jnius_config.add_classpath(PurePOS.class_path)

em_tag = (PurePOS, (), {'source_fields': {'form', 'anas'}, 'target_fields': ['lemma', 'xpostag']})


# emMorph2Dep ##########################################################################################################

from emmorph2ud.emmorph2ud.converter import EmMorph2UD

em_morph2ud = (EmMorph2UD, (), {'source_fields': {'form', 'lemma', 'xpostag'}, 'target_fields': ['upostag', 'feats']})

# emChunk ##############################################################################################################

from HunTag3.huntag.tagger import Tagger as EmSeqTag

model_name = os.path.join(os.path.dirname(__file__), 'HunTag3', 'models', 'maxnp.szeged.emmorph')
cfg_file = os.path.join(os.path.dirname(__file__), 'HunTag3', 'configs', 'maxnp.szeged.emmorph.yaml')
target_field = 'NP-BIO'

em_chunk = (EmSeqTag, ({'cfg_file': cfg_file, 'model_name': model_name},),
            {'source_fields': set(), 'target_fields': [target_field]})

# emNER ################################################################################################################

from HunTag3.huntag.tagger import Tagger as EmSeqTag

model_name = os.path.join(os.path.dirname(__file__), 'HunTag3', 'models', 'ner.szeged.emmorph')
cfg_file = os.path.join(os.path.dirname(__file__), 'HunTag3', 'configs', 'ner.szeged.emmorph.yaml')
target_field = 'NER-BIO'

em_ner = (EmSeqTag, ({'cfg_file': cfg_file, 'model_name': model_name},),
          {'source_fields': set(), 'target_fields': [target_field]})

# emDep ################################################################################################################

from emdeppy.emdeppy import EmDepPy
jnius_config.add_classpath(EmDepPy.class_path)

em_depud = (EmDepPy, (), {'source_fields': {'form', 'lemma', 'upostag', 'feats'},
                          'target_fields': ['id', 'deprel', 'head'],
                          'model_file': os.path.join(os.path.dirname(os.path.abspath(
                              sys.modules[EmDepPy.__module__].__file__)), 'szk.mate.ud.model')})

# emCons ###############################################################################################################

from emconspy.emconspy import EmConsPy
jnius_config.add_classpath(EmConsPy.class_path)
# jnius_config.add_options(EmConsPy.vm_opts)  # Add more memory for the whole REST API
jnius_config.add_options('-Xmx6144m')

em_cons = (EmConsPy, (), {'source_fields': {'form', 'lemma', 'xpostag'},
                          'target_fields': ['cons'],
                          'model_file': os.path.join(os.path.dirname(os.path.abspath(
                              sys.modules[EmConsPy.__module__].__file__)), 'szk.const.model')})

# emCoNLL ##############################################################################################################

from emconll.converter import EmCoNLL

em_conll = (EmCoNLL, (), {'source_fields': {'form'}, 'target_fields': []})

########################################################################################################################

# Map module personalities to firendly names...
tools = {'tok': em_token, 'emToken': em_token,
         'morph': em_morph, 'emMorph': em_morph,
         'pos': em_tag, 'emTag': em_tag,
         'chunk': em_chunk, 'emChunk': em_chunk,
         'ner': em_ner, 'emNER': em_ner,
         'conv-morph': em_morph2ud, 'emmorph2ud': em_morph2ud,
         'dep': em_depud, 'emDep-ud': em_depud,
         'cons': em_cons, 'emCons': em_cons,
         'conll': em_conll, 'emCoNLL': em_conll,
         'dummy-tagger': em_dummy, 'emDummy': em_dummy,
         }

# cat input.txt | ./emtsv.py tok,morph,pos,conv-morph,dep -> cat input.txt | ./emtsv.py tok-dep
presets = {'analyze': ['tok', 'morph', 'pos', 'chunk', 'conv-morph', 'dep', 'cons'],  # Full pipeline
           'tok-morph': ['tok', 'morph'],
           'tok-pos': ['tok', 'morph', 'pos'],
           'tok-chunk': ['tok', 'morph', 'pos', 'chunk'],
           'tok-ner': ['tok', 'morph', 'pos', 'ner'],
           'tok-udpos': ['tok', 'morph', 'pos', 'conv-morph'],
           'tok-dep': ['tok', 'morph', 'pos', 'conv-morph', 'dep'],
           'tok-dep-conll': ['tok', 'morph', 'pos', 'conv-morph', 'dep', 'conll'],
           'tok-cons': ['tok', 'morph', 'pos', 'cons'],
           }

# Store already initialized tools for reuse without reinitialization (singleton store) must explicitly pass it to xtsv
initialised_tools = {}
alias_store = defaultdict(list)
