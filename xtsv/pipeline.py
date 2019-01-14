#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-
import sys
import codecs
from itertools import chain
from collections import defaultdict

from flask import Flask, request, Response, stream_with_context
from flask_restful import Api, Resource
from werkzeug.exceptions import abort

from config import presets, initialised_tools, alias_store
from xtsv.tsvhandler import process


def init_everything(available_tools, init_once=True):  # Init everything properly
    if init_once:
        current_initialised_tools = initialised_tools  # The singleton store
        currrent_alias_store = alias_store
    else:
        current_initialised_tools = {}
        currrent_alias_store = defaultdict(list)

    for prog_name, prog_params in available_tools.items():
        prog, prog_args, prog_kwargs = prog_params
        # Dealias aliases to find the initialized versions
        for inited_prog_name, curr_prog_params in currrent_alias_store[prog]:
            if curr_prog_params == prog_params:
                current_initialised_tools[prog_name] = current_initialised_tools[inited_prog_name]
                break
        else:  # No initialized alias found... Initialize and store as initialized alias!
            current_initialised_tools[prog_name] = prog(*prog_args, **prog_kwargs)  # Inint programs...
            currrent_alias_store[prog].append((prog_name, prog_params))
    return current_initialised_tools


def build_pipeline(inp_stream, used_tools, available_tools, conll_comments=False):
    # Resolve presets to module names to enable shorter URLs...
    if len(used_tools) == 1 and used_tools[0] in presets:
        used_tools = presets[used_tools[0]]

    # Peek header...
    header = next(inp_stream)
    # ...and restore iterator...
    inp_stream = chain([header], inp_stream)

    pipeline_begin = inp_stream
    pipeline_begin_friendly = 'HTTP POST/STDIN file'
    pipeline_begin_prod = set(header.strip().split('\t'))

    pipeline_end = pipeline_begin
    pipeline_end_friendly = pipeline_begin_friendly
    pipeline_prod = pipeline_begin_prod

    for program in used_tools:
        pr = available_tools.get(program)
        if pr is not None:
            if not pr.source_fields.issubset(pipeline_prod):
                raise NameError('ERROR: {0} program requires {1} columns but the previous program {2}'
                                ' has only {3} columns'.format(program, pr.source_fields, pipeline_prod,
                                                               pipeline_end_friendly))
            pipeline_end = process(pipeline_end, pr, conll_comments)
            pipeline_prod |= set(pr.target_fields)
        else:
            raise NameError('ERROR: \'{0}\' program not found. Available programs: {1}'.
                            format(program, sorted(available_tools.keys())))

    return pipeline_end


def add_params(restapi, resource_class, internal_apps, conll_comments):
    if internal_apps is None:
        print('No internal_app is given!', file=sys.stderr)
        exit(1)

    kwargs = {'internal_apps': internal_apps, 'conll_comments': conll_comments}
    # To bypass using self and @route together, default values are at the function declarations
    restapi.add_resource(resource_class, '/', '/<path:path>', resource_class_kwargs=kwargs)


class RESTapp(Resource):
    def get(self, path=''):
        return 'Usage: HTTP POST /tool1/tool2/tool3 e.g: \'{0}\' but suplied \'{1}\' a file' \
               ' mamed as \'file\' in the apropriate TSV format'.format(
                ' or '.join(self._internal_apps.keys()), ' and '.join(path.split('/')))

    def post(self, path):
        if 'file' not in request.files:
            abort(400, 'ERROR: input file not found in request!')

        inp_file = codecs.getreader('UTF-8')(request.files['file'])
        last_prog = ()  # Silence, dummy IDE

        try:
            # TODO: Maybe enable per request setting of allowing conll-style comments
            last_prog = build_pipeline(inp_file, path.split('/'), self._internal_apps, self._conll_comments)
        except NameError as e:
            abort(400, e)

        return Response(stream_with_context((line.encode('UTF-8') for line in last_prog)),
                        direct_passthrough=True)

    def __init__(self, internal_apps=None, conll_comments=False):
        """
        Init REST API class
        :param internal_apps: pre-inicialised applications
        """
        self._internal_apps = internal_apps
        self._conll_comments = conll_comments
        # atexit.register(self._internal_apps.__del__)  # For clean exit...


def pipeline_rest_api(available_tools, name, conll_comments):
    app = Flask(name)
    api = Api(app)
    add_params(api, RESTapp, available_tools, conll_comments)
    return app
