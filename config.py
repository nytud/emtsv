#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os

# DummyTagger (EXAMPLE) ################################################################################################

# Setup the tuple: module name (ending with the filename the class defined in),
# class, friendly name, args (tuple), kwargs (dict)
em_dummy = ('emdummy', 'EmDummy', 'EXAMPLE (The friendly name of DummyTagger used in REST API form)',
            ('Params', 'goes', 'here'),
            {'source_fields': {'form'}, 'target_fields': ['star']})

# emToken ##############################################################################################################

em_token = ('quntoken', 'EmTokenPy', 'emToken', (), {'source_fields': set(),
                                                                'target_fields': ['form', 'wsafter']})

# emMorph ##############################################################################################################

em_morph = ('emmorphpy', 'EmMorphPy', 'emMorph', (), {'source_fields': {'form'}, 'target_fields': ['anas']})

# Hunspell #############################################################################################################

hunspellpy = ('hunspellpy', 'HunspellPy', 'HunspellPy', (),
              {'source_fields': {'form'}, 'target_fields': ['spell', 'hunspell_anas']})

# emTag ################################################################################################################

em_tag = ('purepospy', 'PurePOS', 'emTag (PurePOS)', (),
          {'source_fields': {'form', 'anas'}, 'target_fields': ['lemma', 'xpostag']})

# emMorph2Dep ##########################################################################################################

em_morph2ud = ('emmorph2ud', 'EmMorph2UD', 'emmorph2ud', (),
               {'source_fields': {'form', 'lemma', 'xpostag'}, 'target_fields': ['upostag', 'feats']})

# emChunk ##############################################################################################################

model_name = os.path.join('models', 'maxnp.szeged.emmorph')
cfg_file = os.path.join('configs', 'maxnp.szeged.emmorph.yaml')
target_field = 'NP-BIO'

em_chunk = ('huntag', 'Tagger', 'emChunk', ({'cfg_file': cfg_file, 'model_name': model_name},),
            {'source_fields': set(), 'target_fields': [target_field]})

# emNER ################################################################################################################

model_name = os.path.join('models', 'ner.szeged.emmorph')
cfg_file = os.path.join('configs', 'ner.szeged.emmorph.yaml')
target_field = 'NER-BIO'

em_ner = ('huntag', 'Tagger', 'emNER', ({'cfg_file': cfg_file, 'model_name': model_name},),
          {'source_fields': set(), 'target_fields': [target_field]})

# emDep ################################################################################################################

em_depud = ('emdeppy', 'EmDepPy', 'emDep', (),
            {'source_fields': {'form', 'lemma', 'upostag', 'feats'}, 'target_fields': ['id', 'deprel', 'head']})

# emDep 50 #############################################################################################################

em_depud_50 = ('emdeppy', 'EmDepPy', 'emDep (limited to 50 token)', (),
               {'maxlen': 50,
                'source_fields': {'form', 'lemma', 'upostag', 'feats'}, 'target_fields': ['id', 'deprel', 'head']})

# emCons ###############################################################################################################

em_cons = ('emconspy', 'EmConsPy', 'emCons', (),
           {'source_fields': {'form', 'lemma', 'xpostag'}, 'target_fields': ['cons']})

# emUDPipe tok-parse ###################################################################################################

emudpipe_tok_parse = ('emudpipe', 'UDPipe', 'UDPipe tokenizer, POS tagger and dependency parser as a whole',
                      (), {'task': 'tok-parse', 'source_fields': set(), 'target_fields': ['form', 'lemma', 'upostag',
                           'feats', 'head', 'deprel', 'deps']})

# emUDPipe tok-pos #####################################################################################################

emudpipe_tok_pos = ('emudpipe', 'UDPipe', 'UDPipe tokenizer and POS tagger as a whole',
                    (), {'task': 'tok-pos', 'source_fields': set(),
                         'target_fields': ['form', 'lemma', 'upostag', 'feats']})

# emUDPipe tok #########################################################################################################

emudpipe_tok = ('emudpipe', 'UDPipe', 'UDPipe tokenizer', (),
                {'task': 'tok', 'source_fields': set(), 'target_fields': ['form']})

# emUDPipe pos-parse ###################################################################################################

emudpipe_pos_parse = ('emudpipe', 'UDPipe', 'UDPipe POS tagger and dependency parser as a whole',
                      (), {'task': 'pos-parse', 'source_fields': {'form'},
                           'target_fields': ['lemma', 'upostag', 'feats', 'head', 'deprel', 'deps']})

# emUDPipe pos #########################################################################################################

emudpipe_pos = ('emudpipe', 'UDPipe', 'UDPipe POS tagger', (),
                {'task': 'pos', 'source_fields': {'form'}, 'target_fields': ['lemma', 'upostag', 'feats']})

# emUDPipe parse #######################################################################################################

emudpipe_parse = ('emudpipe', 'UDPipe', 'UDPipe dependency parser',
                  (), {'task': 'parse', 'source_fields': {'form', 'lemma', 'upostag', 'feats'},
                       'target_fields': ['head', 'deprel', 'deps']})

# emCoNLL ##############################################################################################################

em_conll = ('emconll', 'EmCoNLL', 'CoNLL-U converter', (), {'source_fields': {'form'}, 'target_fields': []})

# emTerm ##############################################################################################################

term_list = os.path.join(os.path.dirname(__file__), 'emterm', 'test_termlist.tsv')
em_term = ('emterm', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
           (term_list,), {'source_fields': {'form', 'lemma'}, 'target_fields': ['term']})

# emZero ##############################################################################################################

em_zero = ('emzero', 'EmZero', 'Inserts zero pronouns (subjects, objects and possessors) into dependency parsed texts',
           (), {'source_fields': {'form', 'lemma', 'xpostag', 'upostag', 'feats', 'id', 'head', 'deprel'},
                'target_fields': []})

# emBERT ###############################################################################################################

embert_ner = ('embert.embert', 'EmBERT', 'emBERT', (),
              {'task': 'ner', 'source_fields': {'form'}, 'target_fields': ['NER-BIO']})

embert_basenp = ('embert.embert', 'EmBERT', 'emBERT', (),
                 {'task': 'basenp', 'source_fields': {'form'}, 'target_fields': ['BASE-NP-BIO']})

embert_maxnp = ('embert.embert', 'EmBERT', 'emBERT', (),
                {'task': 'maxnp', 'source_fields': {'form'}, 'target_fields': ['NP-BIO']})

# emIOBUtils ###########################################################################################################

emiobutils_maxnp = ('emiobutils', 'EmIOBUtils', 'IOB format converter and fixer for maxNP', (),
                    {'out_style': 'IOBES', 'source_fields': {'NP-BIO'}, 'target_fields': ['NP-BIO-FIXED']})

emiobutils_ner = ('emiobutils', 'EmIOBUtils', 'IOB format converter and fixer for NER', (),
                  {'out_style': 'IOBES', 'source_fields': {'NER-BIO'}, 'target_fields': ['NER-BIO-FIXED']})

########################################################################################################################

em_gateconv = ('emgateconv', 'EmGATEConv', 'A good-enough converter to GATE format for e-magyar.hu', (),
              {'source_fields': {'form'}})

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
         (em_depud_50, ('dep50', 'emDep-ud50')),
         (em_cons, ('cons', 'emCons')),
         (em_conll, ('conll', 'emCoNLL')),
         (emudpipe_tok, ('udpipe-tok',)),
         (emudpipe_pos, ('udpipe-pos',)),
         (emudpipe_parse, ('udpipe-parse',)),
         (emudpipe_tok_pos, ('udpipe-tok-pos',)),
         (emudpipe_pos_parse, ('udpipe-pos-parse',)),
         (emudpipe_tok_parse, ('udpipe-tok-parse',)),
         (em_term, ('term', 'emTerm',)),
         (em_zero, ('zero', 'emZero')),
         (embert_ner, ('bert-ner', 'emBERT-NER')),
         (embert_basenp, ('bert-basenp', 'emBERT-baseNP')),
         (embert_maxnp, ('bert-np', 'bert-chunk', 'emBERT-NP')),
         (emiobutils_maxnp, ('fix-np', 'fix-chunk', 'emIOBUtils-NP')),
         (emiobutils_ner, ('fix-ner', 'fix-ner', 'emIOBUtils-NER')),
         (em_dummy, ('dummy-tagger', 'emDummy')),
         (em_gateconv, ('gate-conv', 'emGATEConv'))
         ]

# cat input.txt | ./main.py tok,morph,pos,conv-morph,dep -> cat input.txt | ./main.py tok-dep
presets = {'analyze': ('Full pipeline', ['tok', 'morph', 'pos', 'chunk', 'conv-morph', 'dep', 'cons']),
           'tok-morph': ('Raw text to morphologycal analysis', ['tok', 'morph']),
           'tok-pos': ('Raw text to POS-tagging in emMorph formalism', ['tok', 'morph', 'pos']),
           'tok-chunk': ('Raw text to maximal NPs chunking', ['tok', 'morph', 'pos', 'chunk']),
           'tok-ner': ('Raw text to named-entity annotation', ['tok', 'morph', 'pos', 'ner']),
           'tok-udpos': ('Raw text to POS-tagging including UDv1 form', ['tok', 'morph', 'pos', 'conv-morph']),
           'tok-dep': ('Raw text to dependency parsing', ['tok', 'morph', 'pos', 'conv-morph', 'dep']),
           'tok-dep-conll': ('Raw text to dependency parsing in CoNLL-U format',
                             ['tok', 'morph', 'pos', 'conv-morph', 'dep', 'conll']),
           'tok-cons': ('Raw text to constituent parsing', ['tok', 'morph', 'pos', 'cons']),
           'tok-bert-ner': ('Raw text to emBERT named-entity annotation', ['tok', 'bert-ner']),
           'tok-bert-chunk': ('Raw text to emBERT maximal NP chunking', ['tok', 'bert-np']),
           }
