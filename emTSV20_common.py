#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys
import codecs
from itertools import chain

from flask import Flask, request, Response, stream_with_context
from flask_restful import Api, Resource
from werkzeug.exceptions import abort

from TSVRESTTools.tsvhandler import process


def import_pyjnius(class_path):
    """
    PyJNIus can only be imported once per Python interpreter and one must set the classpath before importing...
    """
    # Check if autoclass is already imported...
    if 'autoclass' not in locals() and 'autoclass' not in globals():

        # Tested on Ubuntu 16.04 64bit with openjdk-8 JDK and JRE installed:
        # sudo apt install openjdk-8-jdk-headless openjdk-8-jre-headless

        # Set JAVA_HOME for this session
        try:
            os.environ['JAVA_HOME']
        except KeyError:
            os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'

        os.environ['CLASSPATH'] = ':'.join((class_path, os.environ.get('CLASSPATH', ''))).rstrip(':')

        # Set path and import jnius for this session
        from jnius import autoclass
    else:
        import sys
        from jnius import cast, autoclass  # Dummy autoclass import to silence the IDE
        class_loader = autoclass('java.lang.ClassLoader')
        cl = class_loader.getSystemClassLoader()
        ucl = cast('java.net.URLClassLoader', cl)
        urls = ucl.getURLs()
        cp = ':'.join(url.getFile() for url in urls)

        print('Warning: PyJNIus is already imported with the following classpath: {0}'.format(cp), file=sys.stderr)

    # Return autoclass for later use...
    return autoclass


def import_pyjnius_w_common_classpath(available_tools):
    global _
    # Set potentially required classpaths and import PyJNIus with proper classpaths...
    class_paths = []
    for _, t, *_ in available_tools.values():
        if hasattr(t, 'class_path'):
            class_paths.append(t.class_path)
    class_path = ':'.join(class_paths)
    import_pyjnius(class_path)


def init_everything(available_tools):  # Init everything properly
    import_pyjnius_w_common_classpath(available_tools)
    initialised_tools = {}
    for prog_name, prog_params in available_tools.items():
        _, prog, prog_args, prog_kwargs = prog_params  # Inint programs...
        initialised_tools[prog_name] = prog(*prog_args, **prog_kwargs)
    return initialised_tools


def build_pipeline(inp_stream, used_tools, available_tools):
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
            pipeline_end = process(pipeline_end, pr)
            pipeline_prod |= set(pr.target_fields)
        else:
            raise NameError('ERROR: \'{0}\' program not found. Available programs: {1}'.
                            format(program, sorted(available_tools.keys())))

    return pipeline_end


def add_params(restapi, resource_class, internal_apps):
    if internal_apps is None:
        print('No internal_app is given!', file=sys.stderr)
        exit(1)

    kwargs = {'internal_app': internal_apps}
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
            last_prog = build_pipeline(inp_file, path.split('/'), self._internal_apps)
        except NameError as e:
            abort(400, e)

        return Response(stream_with_context((line.encode('UTF-8') for line in last_prog)),
                        direct_passthrough=True)

    def __init__(self, internal_app=None):
        """
        Init REST API class
        :param internal_app: pre-inicialised applications
        """
        self._internal_apps = internal_app
        # atexit.register(self._internal_apps.__del__)  # For clean exit...


def pipeline_rest_api(available_tools, name):
    app = Flask(name)
    api = Api(app)
    add_params(api, RESTapp, available_tools)
    return app
