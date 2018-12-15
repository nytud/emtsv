#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys

import jnius_config

from xtsv.pipeline import init_everything, build_pipeline, pipeline_rest_api
from config import tools, presets


def import_pyjnius():
    """
    PyJNIus can only be imported once per Python interpreter and one must set the classpath before importing...
    """
    # Check if autoclass is already imported...
    if not jnius_config.vm_running:

        # Tested on Ubuntu 16.04 64bit with openjdk-8 JDK and JRE installed:
        # sudo apt install openjdk-8-jdk-headless openjdk-8-jre-headless

        # Set JAVA_HOME for this session
        try:
            os.environ['JAVA_HOME']
        except KeyError:
            os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'

        # Set path and import jnius for this session
        from jnius import autoclass
    else:
        import sys
        from jnius import cast, autoclass
        class_loader = autoclass('java.lang.ClassLoader')
        cl = class_loader.getSystemClassLoader()
        ucl = cast('java.net.URLClassLoader', cl)
        urls = ucl.getURLs()
        cp = ':'.join(url.getFile() for url in urls)

        print('Warning: PyJNIus is already imported with the following classpath: {0} Please check if it is ok!'.
              format(cp), file=sys.stderr)

    # Return autoclass for later use...
    return autoclass


if __name__ == '__main__':
    autoclass = import_pyjnius()
    if len(sys.argv) > 1:  # TODO: Implement this properly = Argparse
        used_tools = sys.argv[1].split(',')
        if len(used_tools) == 1 and used_tools[0] in presets:
            used_tools = presets[used_tools[0]]  # Resolve presets to module names to init only the needed modules...

        inited_tools = init_everything({k: v for k, v in tools.items() if k in set(used_tools)})
        sys.stdout.writelines(build_pipeline(sys.stdin, used_tools, inited_tools))
    else:
        inited_tools = init_everything(tools)
        app = pipeline_rest_api(inited_tools, name='e-magyar-tsv')
        app.run(debug=True)
