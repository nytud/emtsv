#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from __init__ import init_everything, pipeline_rest_api, jnius_config, tools, presets

jnius_config.classpath_show_warning = False  # Suppress warning
conll_comments = False  # User can enable conll comments for compatibility or disable them for safety per request...
inited_tools = init_everything(tools)
application = pipeline_rest_api(name='e-magyar-tsv', available_tools=inited_tools, presets=presets,
                                conll_comments=conll_comments)
