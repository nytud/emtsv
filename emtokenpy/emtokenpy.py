"""TODO
"""

import subprocess
import os
import tempfile

class EmTokenPy:
    def __init__(self, source_fields=None, target_fields=None):

        # Field names for e-magyar TSV
        if source_fields is None:
            source_fields = {}

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    def process_sentence(self, sen, field_names):
        sen = '\n'.join([x[0] for x in sen])
        with tempfile.NamedTemporaryFile(mode='w') as fh:
            fh.write(sen)
            fh.flush()
            cmd = '{0} -f vert {1}'.format(os.path.join(os.path.dirname(__file__), 'bin', 'quntoken'), fh.name)
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout
            res = res.decode(encoding='utf-8')
            res = res.split('\n')
            res = [[x] for x in res if x]
        return res
        # print(res)
        # return [[]]

    def prepare_fields(self, field_names):
        return field_names
