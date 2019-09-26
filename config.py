#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys


from __init__ import jnius_config

# DummyTagger (EXAMPLE) ################################################################################################

# Import Tagger class, and parameters...
from emdummy.dummytagger import DummyTagger

# Setup the triplet: class, args (tuple), kwargs (dict)
em_dummy = (DummyTagger, 'The friendly name of DummyTagger used in REST API form',
            ('Params', 'goes', 'here'),
            {'source_fields': {'Source field names'}, 'target_fields': ['Target field names']})

# emToken ##############################################################################################################

from emtokenpy.emtokenpy import EmTokenPy

em_token = (EmTokenPy, 'emToken', (), {'source_fields': set(), 'target_fields': ['form']})

# emMorph ##############################################################################################################

from emmorphpy.emmorphpy import EmMorphPy

em_morph = (EmMorphPy, 'emMorph', (), {'source_fields': {'form'}, 'target_fields': ['anas']})

# Hunspell #############################################################################################################

from hunspellpy.hunspellpy import HunspellPy

hunspellpy = (HunspellPy, 'HunspellPy', (), {'source_fields': {'form'}, 'target_fields': ['spell', 'hunspell_anas']})

# emTag ################################################################################################################

from purepospy.purepospy import PurePOS
jnius_config.add_classpath(PurePOS.class_path)

em_tag = (PurePOS, 'emTag (PurePOS)', (), {'source_fields': {'form', 'anas'}, 'target_fields': ['lemma', 'xpostag']})


# emMorph2Dep ##########################################################################################################

from emmorph2ud.emmorph2ud.converter import EmMorph2UD

em_morph2ud = (EmMorph2UD, 'emmorph2ud', (), {'source_fields': {'form', 'lemma', 'xpostag'},
                                              'target_fields': ['upostag', 'feats']})

# emChunk ##############################################################################################################

from HunTag3.huntag.tagger import Tagger as EmSeqTag

model_name = os.path.join(os.path.dirname(__file__), 'HunTag3', 'models', 'maxnp.szeged.emmorph')
cfg_file = os.path.join(os.path.dirname(__file__), 'HunTag3', 'configs', 'maxnp.szeged.emmorph.yaml')
target_field = 'NP-BIO'

em_chunk = (EmSeqTag, 'emChunk', ({'cfg_file': cfg_file, 'model_name': model_name},),
            {'source_fields': set(), 'target_fields': [target_field]})

# emNER ################################################################################################################

from HunTag3.huntag.tagger import Tagger as EmSeqTag

model_name = os.path.join(os.path.dirname(__file__), 'HunTag3', 'models', 'ner.szeged.emmorph')
cfg_file = os.path.join(os.path.dirname(__file__), 'HunTag3', 'configs', 'ner.szeged.emmorph.yaml')
target_field = 'NER-BIO'

em_ner = (EmSeqTag, 'emNER', ({'cfg_file': cfg_file, 'model_name': model_name},),
          {'source_fields': set(), 'target_fields': [target_field]})

# emDep ################################################################################################################

from emdeppy.emdeppy import EmDepPy
jnius_config.add_classpath(EmDepPy.class_path)

em_depud = (EmDepPy, 'emDep', (), {'source_fields': {'form', 'lemma', 'upostag', 'feats'},
                                   'target_fields': ['id', 'deprel', 'head'],
                                   'model_file': os.path.join(os.path.dirname(os.path.abspath(
                                      sys.modules[EmDepPy.__module__].__file__)), 'szk.mate.ud.model')})

# emCons ###############################################################################################################

from emconspy.emconspy import EmConsPy
jnius_config.add_classpath(EmConsPy.class_path)
# jnius_config.add_options(EmConsPy.vm_opts)  # Add more memory for the whole REST API
jnius_config.add_options('-Xmx6144m')

em_cons = (EmConsPy, 'emCons', (), {'source_fields': {'form', 'lemma', 'xpostag'},
                                    'target_fields': ['cons'],
                                    'model_file': os.path.join(os.path.dirname(os.path.abspath(
                                        sys.modules[EmConsPy.__module__].__file__)), 'szk.const.model')})

# emUDPipe tok-parse ###################################################################################################

from emudpipe.emudpipe import UDPipe

emudpipe_tok_parse = (UDPipe, 'UDPipe tokenizer', (), {'task': 'tok-parse', 'source_fields': set(),
                                                       'target_fields': ['form', 'lemma', 'upostag',
                                                                         'feats', 'head', 'deprel', 'deps']})

# emUDPipe tok-pos #####################################################################################################

from emudpipe.emudpipe import UDPipe

emudpipe_tok_pos = (UDPipe, 'UDPipe tokenizer & POS tagger', (), {'task': 'tok-pos', 'source_fields': set(),
                                                                  'target_fields': ['form', 'lemma', 'upostag',
                                                                                    'feats']})

# emUDPipe tok #########################################################################################################

from emudpipe.emudpipe import UDPipe

emudpipe_tok = (UDPipe, 'UDPipe tokenizer', (), {'task': 'tok', 'source_fields': set(),
                                                 'target_fields': ['form']})

# emUDPipe pos-parse ###################################################################################################

from emudpipe.emudpipe import UDPipe

emudpipe_pos_parse = (UDPipe, 'UDPipe POS tagger & dependeny parser',
                      (), {'task': 'pos-parse', 'source_fields': {'form'},
                           'target_fields': ['lemma', 'upostag', 'feats', 'head', 'deprel', 'deps']})

# emUDPipe pos #########################################################################################################

from emudpipe.emudpipe import UDPipe

emudpipe_pos = (UDPipe, 'UDPipe POS tagger', (), {'task': 'pos', 'source_fields': {'form'},
                                                  'target_fields': ['lemma', 'upostag', 'feats']})

# emUDPipe parse #######################################################################################################

from emudpipe.emudpipe import UDPipe

emudpipe_parse = (UDPipe, 'UDPipe dependency parser',
                  (), {'task': 'parse', 'source_fields': {'form', 'lemma', 'upostag', 'feats'},
                       'target_fields': ['head', 'deprel', 'deps']})

# emCoNLL ##############################################################################################################

from emconll.converter import EmCoNLL

em_conll = (EmCoNLL, 'CoNLL-U converter', (), {'source_fields': {'form'}, 'target_fields': []})

########################################################################################################################

# Map module personalities to firendly names...
# The first name is the default. The order is the display order of the modules
tools = [(em_token, ('tok', 'emToken')),
         (em_morph, ('morph', 'emMorph')),
         (hunspellpy, ('spell', 'hunspell')),
         (em_tag, ('pos', 'emTag')),
         (em_chunk, ('chunk', 'emChunk')),
         (em_ner, ('ner', 'emNER')),
         (em_morph2ud, ('conv-morph', 'emmorph2ud')),
         (em_depud, ('dep', 'emDep-ud')),
         (em_cons, ('cons', 'emCons')),
         (em_conll, ('conll', 'emCoNLL')),
         (em_dummy, ('dummy-tagger', 'emDummy')),
         (emudpipe_tok_parse, ('udpipe-tok-parse',)),
         (emudpipe_tok_pos, ('udpipe-tok-pos',)),
         (emudpipe_tok, ('udpipe-tok',)),
         (emudpipe_pos_parse, ('udpipe-pos-parse',)),
         (emudpipe_pos, ('udpipe-pos',)),
         (emudpipe_parse, ('udpipe-parse',)),
         ]

# cat input.txt | ./main.py tok,morph,pos,conv-morph,dep -> cat input.txt | ./main.py tok-dep
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
