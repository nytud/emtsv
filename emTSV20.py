#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

from TSVRESTTools.tsvhandler import process


def get_emmorph():
    from emMorphREST import em_morph
    # TODO: em_morph.required
    return {'string'}, set(em_morph.target_fields), em_morph


def get_emtag():
    from emTagREST import em_tag
    # TODO: em_tag.required
    return {'string', 'anas'}, set(em_tag.target_fields), em_tag


def get_deptool():  # TODO: Some java classpath error!
    from depToolREST import dt
    # TODO: dt.required
    return {'string', 'lemma', 'hfstana'}, set(dt.target_fields), dt


def get_emchunk():
    from emChunkREST import em_chunk
    # TODO: em_chunk.required
    return {'string', 'lemma', 'hfstana'}, set(em_chunk.target_fields), em_chunk


def get_emdep():
    from emDepREST import em_dep
    # TODO: em_dep.required
    return {'string', 'lemma', 'pos', 'feature'}, set(em_dep.target_fields), em_dep


tools = {'morph': get_emmorph, 'pos': get_emtag, 'deptool': get_deptool, 'chunk': get_emchunk, 'dep': get_emdep}


def build_pipeline(inp_stream, used_tools, available_tools):
    pipeline_begin = inp_stream
    pipeline_begin_friendly = 'HTTP POST file'

    pipeline_end = pipeline_begin
    pipeline_end_friendly = pipeline_begin_friendly
    pipeline_prod = {'string'}

    for prog in used_tools:
        p = available_tools.get(prog)
        if prog is not None:
            reqv, prod, pr = p()
            if not reqv.issubset(pipeline_prod):
                return abort(404, Response(
                    'ERROR: {0} program requires {1} columns but the previous program {2} has only {3} columns'.
                    format(prog, reqv, pipeline_prod, pipeline_end_friendly)))
            pipeline_end = process(pipeline_end, pr)
            pipeline_prod |= prod

    return pipeline_end


if __name__ == '__main__':
    if len(sys.argv) > 1:  # TODO: Implement this properly
        sys.stdout.writelines(build_pipeline(sys.stdin, sys.argv[1].split(','), tools))
    else:
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
            restapi.add_resource(RESTapp, '/<path:path>', resource_class_kwargs=kwargs)


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
