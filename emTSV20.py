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

if __name__ == '__main__':
    if len(sys.argv) > 1:  # TODO: Implement this properly
        pipeline_begin = open('ide2.txt', encoding='UTF-8')  # sys.stdin
        pipeline_begin_friendly = 'STDIN'

        pipeline_end = pipeline_begin
        pipeline_end_friendly = pipeline_begin_friendly
        pripeline_reqv = {'string'}
        pipeline_prod = {'string'}

        for prog in sys.argv[1].split(','):
            p = tools.get(prog)
            if prog is not None:
                reqv, prod, pr = p()
                if not reqv.issubset(pipeline_prod):
                    print('ERROR: {0} program requires {1} columns but the previous program {2} has only {3} columns'.
                          format(prog, reqv, pipeline_prod, pipeline_end_friendly))
                    exit(1)
                pipeline_end = process(pipeline_end, pr)
                pipeline_prod |= prod

        sys.stdout.writelines(pipeline_end)
    else:
        pass  # TODO: Same in flask. Per request build pipeline like above and stream the output...
              # TODO: e.g. 127.0.0.1:5000/morph/pos/chunk
