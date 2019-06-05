#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from os.path import isfile
from argparse import ArgumentParser, ArgumentTypeError, REMAINDER

from __init__ import init_everything, build_pipeline, pipeline_rest_api, jnius_config, import_pyjnius, tools, presets


def valid_file(input_file):
    if not isfile(input_file):
        raise ArgumentTypeError('"{0}" must be a file!'.format(input_file))
    return input_file


def str2bool(v):
    """
    Original code from:
     https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse/43357954#43357954
    """
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input_filename', type=valid_file,
                        help='Use input file instead of STDIN',
                        metavar='FILE')
    parser.add_argument('-o', '--output', dest='output_filename',
                        help='Use output file instead of STDOUT',
                        metavar='FILE')
    parser.add_argument('-v', '--verbose', dest='verbose', type=str2bool, nargs='?', const=True, default=False,
                        help='Show warnings',
                        metavar='BOOL')
    parser.add_argument('-c', '--conllu-comments', dest='comments', type=str2bool, nargs='?', const=True, default=False,
                        help='Enable CoNLL-U style comments',
                        metavar='BOOL')
    parser.add_argument(dest='task', nargs=REMAINDER)

    options = parser.parse_args()
    # Set input and output stream...
    if options.input_filename:
        options.input_stream = open(options.input_filename, encoding='UTF-8')
    else:
        options.input_stream = sys.stdin

    if options.output_filename:
        options.output_stream = open(options.output_filename, 'w', encoding='UTF-8')
    else:
        options.output_stream = sys.stdout

    return options


if __name__ == '__main__':

    opts = parse_args()

    input_iterator = opts.input_stream
    output_iterator = opts.output_stream
    autoclass = import_pyjnius()
    jnius_config.classpath_show_warning = opts.verbose  # Suppress warning.
    conll_comments = opts.comments
    if len(opts.task) > 0:
        used_tools = opts.task[0].split(',')
        if len(used_tools) == 1 and used_tools[0] in presets:
            used_tools = presets[used_tools[0]]  # Resolve presets to module names to init only the needed modules...

        inited_tools = init_everything({k: v for k, v in tools.items() if k in set(used_tools)})
        output_iterator.writelines(build_pipeline(input_iterator, used_tools, inited_tools, presets, conll_comments))
    else:
        inited_tools = init_everything(tools)
        app = pipeline_rest_api(name='e-magyar-tsv', available_tools=inited_tools, presets=presets,
                                conll_comments=conll_comments)
        app.run(debug=True)
