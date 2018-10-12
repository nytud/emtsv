#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import codecs
import sys

import atexit


from flask import Flask, request, url_for, Response, stream_with_context
from flask_restful import Api, Resource
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from TSVRESTTools.tsvhandler import process  # Only this is needed from the TSV handler...


def create_app(name, command, internal_app):
    app = Flask(name)
    api = Api(app)
    add_params(api, command, internal_app)

    return app


def add_params(restapi, command, internal_app):
    if internal_app is None:
        print('No internal_app is given!', file=sys.stderr)
        exit(1)

    kwargs = {'command': command, 'internal_app': internal_app}
    # To bypass using self and @route together
    restapi.add_resource(RESTapp, *('/', command), resource_class_kwargs=kwargs)


class RESTapp(Resource):
    def get(self):
        return 'Usage: HTTP POST {0} a file mamed as \'file\' in the apropriate TSV format'.format(self._command)

    def post(self):
        if not request.path.endswith(self._command):
            return redirect(url_for('restapp'), '301')
        if 'file' not in request.files:
            abort(400)
        inp_file = codecs.getreader('UTF-8')(request.files['file'])
        return Response(stream_with_context((line.encode('UTF-8') for line in process(inp_file, self._internal_app))),
                        direct_passthrough=True)

    def __init__(self, command, internal_app=None):
        """
        Init REST API class
        :param command: the command to answer (parse, tag, analyze, etc.)
        :param internal_app: pre-inicialised application
        """
        self._command = command
        self._internal_app = internal_app
        # atexit.register(self._internal_app.__del__)  # For clean exit...
