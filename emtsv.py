#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

import jnius_config

from __init__ import init_everything, build_pipeline, pipeline_rest_api, import_pyjnius, tools, presets


if __name__ == '__main__':
    autoclass = import_pyjnius()
    jnius_config.classpath_show_warning = False  # Suppress warning. # TODO: Add --verbose CLI option for this warning!
    conll_comments = False  # TODO: Allow conll comments for compatibility or disable them for safety...
    if len(sys.argv) > 1:  # TODO: Implement this properly = Argparse
        used_tools = sys.argv[1].split(',')
        if len(used_tools) == 1 and used_tools[0] in presets:
            used_tools = presets[used_tools[0]]  # Resolve presets to module names to init only the needed modules...

        inited_tools = init_everything({k: v for k, v in tools.items() if k in set(used_tools)})
        sys.stdout.writelines(build_pipeline(sys.stdin, used_tools, inited_tools, conll_comments))
    else:
        inited_tools = init_everything(tools)
        app = pipeline_rest_api(inited_tools, name='e-magyar-tsv', conll_comments=conll_comments)
        app.run(debug=True)
