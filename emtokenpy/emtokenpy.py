#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

"""Python wrapper for quntoken.
"""

from quntoken import tokenize


class EmTokenPy:
    pass_header = True

    def __init__(self, source_fields=None, target_fields=None):

        # Field names for e-magyar TSV
        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    @staticmethod
    def process_sentence(sen, _=None):
        cmd = ['preproc', 'snt', 'sntcorr', 'sntcorr', 'token', 'convtsv']
        res = tokenize(cmd, sen)
        return res

    @staticmethod
    def prepare_fields(field_names):
        return field_names

