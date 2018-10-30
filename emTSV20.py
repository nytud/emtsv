#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from itertools import chain


from personalities import tools, import_pyjnius_fun
from TSVRESTTools.tsvhandler import process

# Set potentially required classpaths and import PyJNIus with proper classpaths...
class_paths = []
for _, t, *_ in tools.values():
    if hasattr(t, 'class_path'):
        class_paths.append(t.class_path)

class_path = ':'.join(class_paths)

autoclass = import_pyjnius_fun(class_path)


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

    for prog in used_tools:
        p = available_tools.get(prog)
        if p is not None:
            # Inint programs...
            _, tagger, args, kwargs = p
            pr = tagger(*args, **kwargs)
            if not pr.source_fields.issubset(pipeline_prod):
                raise NameError('ERROR: {0} program requires {1} columns but the previous program {2}'
                                ' has only {3} columns'.format(prog, pr.source_fields, pipeline_prod,
                                                               pipeline_end_friendly))
            pipeline_end = process(pipeline_end, pr)
            pipeline_prod |= set(pr.target_fields)

    return pipeline_end


def pipeline_rest_api():
    # TODO: Implement this properly
    import codecs
    import sys
    from flask import Flask, request, Response, stream_with_context
    from flask_restful import Api, Resource
    from werkzeug.exceptions import abort

    def add_params(restapi, _, internal_apps):
        if internal_apps is None:
            print('No internal_app is given!', file=sys.stderr)
            exit(1)

        kwargs = {'internal_app': internal_apps}
        # To bypass using self and @route together
        # TODO: / is not handled...
        """
        This works...
        app.add_url_rule('/<path:path>', 'catch_all', catch_all, defaults={'path': ''})
        app.add_url_rule('/', 'catch_all', catch_all, defaults={'path': ''})
        """
        restapi.add_resource(RESTapp, '/', '/<path:path>', defaults={'path': ''}, resource_class_kwargs=kwargs)

    class RESTapp(Resource):
        def get(self, path):
            return 'Usage: HTTP POST /tool1/tool2/tool3 e.g: {0} but suplied {1} a file' \
                   ' mamed as \'file\' in the apropriate TSV format'.format(
                    ' or '.join(self._internal_apps.keys()), ' and '.join(path.split('/')))

        def post(self, path):
            if 'file' not in request.files:
                abort(400)
            inp_file = codecs.getreader('UTF-8')(request.files['file'])
            last_prog = build_pipeline(inp_file, path.split('/'), self._internal_apps)
            # TODO: This shared code wit the CLI version. Should be movet to a funciton...

            return Response(
                stream_with_context((line.encode('UTF-8') for line in last_prog)),
                direct_passthrough=True)

        def __init__(self, internal_app=None):
            """
            Init REST API class
            :param internal_app: pre-inicialised application
            """
            self._internal_apps = internal_app
            # atexit.register(self._internal_apps.__del__)  # For clean exit...

    name = 'emTSV20'
    app = Flask(name)
    api = Api(app)
    add_params(api, '/', tools)
    app.run(debug=True)


if __name__ == '__main__':
    if len(sys.argv) > 1:  # TODO: Implement this properly
        sys.stdout.writelines(build_pipeline(sys.stdin, sys.argv[1].split(','), tools))
    else:
        pipeline_rest_api()
