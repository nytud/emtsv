#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys
from collections import defaultdict

import jnius_config

# DummyTagger (EXAMPLE) ################################################################################################

# Import Tagger class, and parameters...
sys.path.append(os.path.join(os.path.dirname(__file__), 'Dummy'))  # Needed to be able to use git submodule...
from DummyTagger.dummy import DummyTagger

# Setup the triplet: class, args (tuple), kwargs (dict)
dummy_tagger = (DummyTagger, ('Params', 'goes', 'here'),
                {'source_fields': {'Source field names'}, 'target_fields': ['Target field names']})

# emToken ##############################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emtokenpy'))  # Needed to be able to use git submodule...
from emtokenpy import EmTokenPy

em_token = (EmTokenPy, (), {'source_fields': set(), 'target_fields': ['form']})

# emMorph ##############################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emmorphpy'))  # Needed to be able to use git submodule...
from emmorphpy import EmMorphPy

em_morph = (EmMorphPy, (), {'source_fields': {'form'}, 'target_fields': ['anas']})

# emTag ################################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'purepospy'))  # Needed to be able to use git submodule...
from purepospy import PurePOS
jnius_config.add_classpath(PurePOS.class_path)

em_tag = (PurePOS, (), {'source_fields': {'form', 'anas'}, 'target_fields': ['lemma', 'xpostag']})

# emDepTool ############################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'deptoolpy'))  # Needed to be able to use git submodule...
from deptoolpy.deptoolpy import DepToolPy
jnius_config.add_classpath(DepToolPy.class_path)

em_deptool = (DepToolPy, (), {'source_fields': {'form', 'lemma', 'xpostag'}, 'target_fields': ['upostag', 'feats']})

# emMorph2Dep ##########################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emmorph2ud'))  # Needed to be able to use git submodule...
from emmorph2ud.converter import EmMorph2UD

em_morph2ud = (EmMorph2UD, (), {'source_fields': {'form', 'lemma', 'xpostag'}, 'target_fields': ['upostag', 'feats']})

# emChunk ##############################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'HunTag3'))
from huntag.tagger import Tagger as EmSeqTag

model_name = os.path.join(os.path.dirname(__file__), 'HunTag3', 'models', 'maxnp.szeged.emmorph')
cfg_file = os.path.join(os.path.dirname(__file__), 'HunTag3', 'configs', 'maxnp.szeged.emmorph.yaml')
target_field = 'NP-BIO'

em_chunk = (EmSeqTag, ({'cfg_file': cfg_file, 'model_name': model_name},),
            {'source_fields': set(), 'target_fields': [target_field]})

# emNER ################################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'HunTag3'))
from huntag.tagger import Tagger as EmSeqTag

model_name = os.path.join(os.path.dirname(__file__), 'HunTag3', 'models', 'ner.szeged.emmorph')
cfg_file = os.path.join(os.path.dirname(__file__), 'HunTag3', 'configs', 'ner.szeged.emmorph.yaml')
target_field = 'NP-BIO'

em_ner = (EmSeqTag, ({'cfg_file': cfg_file, 'model_name': model_name},),
          {'source_fields': set(), 'target_fields': [target_field]})

# emDep ################################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emdeppy'))  # Needed to be able to use git submodule...
from emdeppy import EmDepPy
jnius_config.add_classpath(EmDepPy.class_path)

em_dep = (EmDepPy, (), {'source_fields': {'form', 'lemma', 'upostag', 'feats'},
                        'target_fields': ['id', 'deprel', 'head']})

# emDep ################################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emdeppy'))  # Needed to be able to use git submodule...
from emdeppy import EmDepPy
jnius_config.add_classpath(EmDepPy.class_path)

em_depud = (EmDepPy, (), {'source_fields': {'form', 'lemma', 'upostag', 'feats'},
                          'target_fields': ['id', 'deprel', 'head'],
                          'model_file': os.path.join(os.path.dirname(os.path.abspath(
                              sys.modules[EmDepPy.__module__].__file__)), 'szk.mate.ud.model')})

# emCons ###############################################################################################################

sys.path.append(os.path.join(os.path.dirname(__file__), 'emconspy'))  # Needed to be able to use git submodule...
from emconspy import EmConsPy
jnius_config.add_classpath(EmConsPy.class_path)
# jnius_config.add_options(EmConsPy.vm_opts)  # Add more memory for the whole REST API
jnius_config.add_options('-Xmx6144m')

em_cons = (EmConsPy, (), {'source_fields': {'form', 'lemma', 'xpostag'},
                          'target_fields': ['cons'],
                          'model_file': os.path.join(os.path.dirname(os.path.abspath(
                              sys.modules[EmConsPy.__module__].__file__)), 'szk.const.model')})

########################################################################################################################

# Map module personalities to firendly names...
tools = {'tok': em_token, 'emToken': em_token,
         'morph': em_morph, 'emMorph': em_morph,
         'pos': em_tag, 'emTag': em_tag,
         'chunk': em_chunk, 'emChunk': em_chunk,
         'ner': em_ner, 'emNER': em_ner,
         # Default is UD
         'conv-morph': em_morph2ud, 'conv-hfst2ud': em_morph2ud, 'conv-hfst2conll': em_deptool, 'emDepTool': em_deptool,
         'dep': em_depud, 'emDep-ud': em_depud, 'emDep-conll': em_dep, 'emDep': em_dep,
         'cons': em_cons, 'emCons': em_cons,
         }

presets = {'analyze': ['tok', 'morph', 'pos', 'chunk', 'conv-morph', 'dep', 'cons'],  # Full pipeline
           'tok-morph': ['tok', 'morph'],
           'tok-pos': ['tok', 'morph', 'pos'],
           'tok-chunk': ['tok', 'morph', 'pos', 'chunk'],
           'tok-ner': ['tok', 'morph', 'pos', 'ner'],
           'tok-dep': ['tok', 'morph', 'pos', 'conv-morph', 'dep'],
           'tok-dep-conll': ['tok', 'morph', 'pos', 'emDepTool', 'emDep-conll'],
           'tok-cons': ['tok', 'morph', 'pos', 'cons'],
           }

# Store already initialized tools for later reuse without reinitialization (singleton store)
initialised_tools = {}
alias_store = defaultdict(list)

# cat input.txt | ./emtsv.py tok,morph,pos,conv-morph,dep -> cat input.txt | ./emtsv.py tok-dep
