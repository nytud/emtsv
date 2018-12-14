#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-


class DummyTagger:
    class_path = ''  # TODO: Fill this variable if module requires JAVA...

    def __init__(self, source_fields=None, target_fields=None):

        # Field names for e-magyar TSV
        if source_fields is None:
            source_fields = {}

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields           # TODO: Implement or overload on inherit

    def process_sentence(self, sen, field_names):
        return sen                                   # TODO: Implement or overload on inherit

    def prepare_fields(self, field_names):
        return field_names                           # TODO: Implement or overload on inherit
