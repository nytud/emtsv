#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from __init__ import singleton_store_factory, pipeline_rest_api, jnius_config, tools, presets

jnius_config.classpath_show_warning = False  # Suppress warning
conll_comments = False  # User can enable conll comments for compatibility or disable them for safety per request...
singleton_store = singleton_store_factory()
application = pipeline_rest_api(name='e-magyar-tsv', available_tools=tools, presets=presets,
                                conll_comments=conll_comments, singleton_store=singleton_store,
                                form_title='e-magyar text processing system',
                                doc_link='https://github.com/dlt-rilmta/emtsv')
