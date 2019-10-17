#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

from __init__ import build_pipeline, pipeline_rest_api, jnius_config, parser_skeleton, tools, presets, \
    singleton_store_factory

if __name__ == '__main__':

    argparser = parser_skeleton(description='emtsv -- e-magyar language processing system')
    opts = argparser.parse_args()

    jnius_config.classpath_show_warning = opts.verbose  # Suppress warning.
    conll_comments = opts.conllu_comments
    if len(opts.task) > 0:
        if opts.input_text is not None:
            input_data = opts.input_text
        else:
            input_data = opts.input_stream
        output_iterator = opts.output_stream

        used_tools = opts.task.split(',')
        output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets, conll_comments))
    elif (opts.input_stream == sys.stdin and opts.input_text is None) and opts.output_stream == sys.stdout:
        singleton_store = singleton_store_factory()
        app = pipeline_rest_api(name='e-magyar-tsv', available_tools=tools, presets=presets,
                                conll_comments=conll_comments, singleton_store=singleton_store,
                                form_title='e-magyar text processing system',
                                doc_link='https://github.com/dlt-rilmta/emtsv')
        app.run(debug=True)
    else:
        argparser.error('In REST mode, input and output are supressed, '
                        'so -i and -o are allowed allowed only when at least one task is specified.')
