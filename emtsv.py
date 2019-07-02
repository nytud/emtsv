#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from argparse import ArgumentParser
import sys

from __init__ import init_everything, build_pipeline, pipeline_rest_api, jnius_config, parser_skeleton, tools, presets


def parse_arguments():
    """
    Parses the command-line arguments. Adds an additional switch to
    :func:`xtsv.parser_skeleton`.
    """
    parent = parser_skeleton(
        description='emtsv -- e-magyar language processing system')
    parser = ArgumentParser(parents=[parent], add_help=False)
    parser.add_argument('--rest', action='store_true',
                        help='Run the REST server. This option supresses any '
                             'input or output (see -i and -o)')
    args = parser.parse_args()
    if args.rest and (args.input_stream != sys.stdin or args.output_stream != sys.stdout):
        parser.error('In REST mode, input and output are supressed, so '
                     '-i and -o are not allowed.')
    return args


if __name__ == '__main__':
    opts = parse_arguments()

    jnius_config.classpath_show_warning = opts.verbose  # Suppress warning.
    conll_comments = opts.conllu_comments

    if len(opts.task) > 0:
        used_tools = opts.task[0].split(',')
        if len(used_tools) == 1 and used_tools[0] in presets:
            used_tools = presets[used_tools[0]]  # Resolve presets to module names to init only the needed modules...

        inited_tools = init_everything({k: v for k, v in tools.items() if k in set(used_tools)})
    else:
        inited_tools = init_everything(tools)

    if not opts.rest:
        input_iterator = opts.input_stream
        output_iterator = opts.output_stream

        pipeline = build_pipeline(input_iterator, used_tools,
                                  inited_tools, presets, conll_comments)
        output_iterator.writelines(pipeline)
    else:
        app = pipeline_rest_api(name='e-magyar-tsv', available_tools=inited_tools,
                                presets=presets, conll_comments=conll_comments)
        app.run(debug=True)
