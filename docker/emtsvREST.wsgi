#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from __init__ import init_everything, pipeline_rest_api, jnius_config, import_pyjnius, tools, presets

autoclass = import_pyjnius()
jnius_config.classpath_show_warning = False  # Suppress warning. # TODO: Add --verbose CLI option for this warning!
conll_comments = False  # TODO: Allow conll comments for compatibility or disable them for safety...
inited_tools = init_everything(tools)
application = pipeline_rest_api(name='e-magyar-tsv', available_tools=inited_tools, presets=presets,
                                conll_comments=conll_comments)
