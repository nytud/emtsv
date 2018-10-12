#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-


class DummyTagger:
    def __init__(self):
        self.target_fields = ['target', 'target2']  # TODO: Implement or overload on inherit

    def process_sentence(self, sen, field_names):
        return sen                                   # TODO: Implement or overload on inherit

    def prepare_fields(self, field_names):
        return field_names                           # TODO: Implement or overload on inherit
