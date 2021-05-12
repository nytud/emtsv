"""Testing emtsv

- library
- CLI
- REST API
- docker CLI
- docker REST API
"""
import pytest
import sys
from glob import glob


def get_ios():
    """Return list of (input, output, gold) filename triplets.
    """
    files = []
    input_files = glob('./tests/input/*')
    gold_files = glob('./tests/gold/*')
    files.append(input_files)
    files.append(gold_files)
    return files

def test_lib():
    # from ..main import build_pipeline, jnius_config, tools, presets, pipeline_rest_api, singleton_store_factory
    # with open('tests/input/alaptorveny.txt') as inp:
    #     input_data = iter(inp.readlines())
    # output_iterator = sys.stdout
    # used_tools = ['tok', 'morph', 'pos']
    # # used_tools = ['tok']
    # conll_comments = True
    # output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets, conll_comments))
    print(get_ios())
    assert False
