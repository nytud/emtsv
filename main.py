#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

from __init__ import build_pipeline, pipeline_rest_api, jnius_config, parser_skeleton, tools, presets, \
    singleton_store_factory

import npyscreen


def download():
    F = npyscreen.Form(name="Download models",)
    ms2 = F.add(npyscreen.TitleMultiSelect, max_height=-2, value=[1, ], name="Pick Several",
                values=["Option1", "Option2", "Option3"], scroll_exit=True)

if __name__ == '__main__':

    argparser = parser_skeleton(description='emtsv -- e-magyar language processing system')
    opts = argparser.parse_args()

    jnius_config.classpath_show_warning = opts.verbose  # Suppress warning.
    conll_comments = opts.conllu_comments
    if len(opts.task) > 0:
        input_iterator = opts.input_stream
        output_iterator = opts.output_stream

        used_tools = opts.task[0].split(',')
        output_iterator.writelines(build_pipeline(input_iterator, used_tools, tools, presets, conll_comments))
    elif opts.input_stream == sys.stdin or opts.output_stream == sys.stdout:
        singleton_store = singleton_store_factory()
        app = pipeline_rest_api(name='e-magyar-tsv', available_tools=tools, presets=presets,
                                conll_comments=conll_comments, singleton_store=singleton_store,
                                form_title='e-magyar text processing system',
                                doc_link='https://github.com/dlt-rilmta/emtsv')
        app.run(debug=True)
    else:
        argparser.error('In REST mode, input and output are supressed, '
                        'so -i and -o are allowed allowed only when at least one task is specified.')
