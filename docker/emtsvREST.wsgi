#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import jnius_config

from __init__ import init_everything, pipeline_rest_api, import_pyjnius, tools


autoclass = import_pyjnius()
jnius_config.classpath_show_warning = False  # Suppress warning. # TODO: Add --verbose CLI option for this warning!
conll_comments = False  # TODO: Allow conll comments for compatibility or disable them for safety...
inited_tools = init_everything(tools)
application = pipeline_rest_api(inited_tools, name='e-magyar-tsv', conll_comments=conll_comments)
