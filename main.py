#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

from __init__ import init_everything, build_pipeline, pipeline_rest_api, jnius_config, parser_skeleton, tools, presets

if __name__ == '__main__':

    argparser = parser_skeleton(description='emtsv -- e-magyar language processing system')
    opts = argparser.parse_args()

    jnius_config.classpath_show_warning = opts.verbose  # Suppress warning.
    conll_comments = opts.conllu_comments
    if len(opts.task) > 0:
        input_iterator = opts.input_stream
        output_iterator = opts.output_stream

        used_tools = opts.task[0].split(',')
        if len(used_tools) == 1 and used_tools[0] in presets:
            used_tools = presets[used_tools[0]]  # Resolve presets to module names to init only the needed modules...

        inited_tools = init_everything({k: v for k, v in tools.items() if k in set(used_tools)})
        output_iterator.writelines(build_pipeline(input_iterator, used_tools, inited_tools, presets, conll_comments))
    elif opts.input_stream == sys.stdin or opts.output_stream == sys.stdout:
        inited_tools = init_everything(tools)
        app = pipeline_rest_api(name='e-magyar-tsv', available_tools=inited_tools, presets=presets,
                                conll_comments=conll_comments)
        app.run(debug=True)
    else:
        argparser.error('In REST mode, input and output are supressed, '
                        'so -i and -o are allowed allowed only when at least one task is specified.')
