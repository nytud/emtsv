import sys
import os

sys.path.append(os.path.dirname(__file__))

from xtsv.pipeline import init_everything, build_pipeline, pipeline_rest_api
from xtsv.tsvhandler import process
from config import tools, presets

import jnius_config


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
    elif hasattr(jnius_config, 'classpath_show_warning') and not jnius_config.classpath_show_warning:
        from jnius import autoclass  # Warning already had shown. It is enough to show it only once!
    else:
        import sys
        from jnius import cast, autoclass
        class_loader = autoclass('java.lang.ClassLoader')
        cl = class_loader.getSystemClassLoader()
        ucl = cast('java.net.URLClassLoader', cl)
        urls = ucl.getURLs()
        cp = ':'.join(url.getFile() for url in urls)

        jnius_config.classpath_show_warning = False
        print('Warning: PyJNIus is already imported with the following classpath: {0} Please check if it is ok!'.
              format(cp), file=sys.stderr)

    # Return autoclass for later use...
    return autoclass
