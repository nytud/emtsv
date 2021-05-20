"""Testing emtsv

- library
- CLI
- REST API
- docker CLI
- docker REST API
"""
# import pytest
# import sys
# from tempfile import mkdtemp
# from shutil import rmtree
from pathlib import Path


class Case:
    def __init__(self, input_path, gold_path) -> None:
        self.input_path = input_path
        self.gold_path = gold_path
        self.outout_path = self.get_output_path()
        self.modules = self.get_modules()
    
    def __str__(self) -> str:
        return f'inp: {self.input_path}\ngold: {self.gold_path}\n'

    def get_output_path(self) -> str:
        return '/output/valami.tsv'

    def get_modules(self) -> list:
        return ['tok', 'morph', 'pos']


def get_modules(input_path: str, gold_path: str) -> list:
    """Return with list of modules needed for the gold.

    Return with an empty list, if the gold cannot be produced.
    """
    modules = []
    input_parts = Path(input_path).name.split('.')
    gold_parts = Path(gold_path).name.split('.')
    print(input_parts)
    print(gold_parts)
    print()
    return modules


def generate_cases():
    """Return list of (input, output, gold) filename triplets.
    """
    # outdir = mkdtemp()
    # rmtree(outdir)
    tests_dir = Path('./tests')
    inp_files = list(tests_dir.glob('input/*'))
    gold_files = list(tests_dir.glob('gold/*'))
    cases = []
    for i in inp_files:
        for g in gold_files:
            if get_modules(i, g):
                cases.append(Case(i, g))
    for c in cases:
        pass
        # print(c)
    # print(inp_files)
    # print(gold_files)

def test_lib():
    # from ..main import build_pipeline, jnius_config, tools, presets, pipeline_rest_api, singleton_store_factory
    # with open('tests/input/alaptorveny.txt') as inp:
    #     input_data = iter(inp.readlines())
    # output_iterator = sys.stdout
    # used_tools = ['tok', 'morph', 'pos']
    # # used_tools = ['tok']
    # conll_comments = True
    # output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets, conll_comments))
    print(generate_cases())
    assert False

if __name__ == '__main__':
    generate_cases()
