"""Testing emtsv

- library
- CLI
- REST API
- docker CLI
- docker REST API
"""
# import pytest
from tempfile import mkdtemp
from pathlib import Path
from collections import namedtuple


Case = namedtuple('Case', 'input_path, gold_path, modules, output_path')
OUTDIR = mkdtemp()


def get_modules(input_path: str, gold_path: str) -> list:
    """Return with list of modules needed for the gold.

    Return with an empty list, if the gold cannot be produced.
    """
    modules = []
    input_parts = Path(input_path).name.split('.')
    gold_parts = Path(gold_path).name.split('.')
    # sanity check
    input_length = len(input_parts)
    gold_length = len(gold_parts)
    assert (input_length == 2 and input_parts[-1] == 'txt') or \
        (input_length == 3 and input_parts[-1] == 'tsv'), \
        f'wrong input file name ({Path(input_path)})'
    assert gold_length == 3 and gold_parts[-1] == 'tsv', \
        f'wrong gold file name ({Path(gold_path)})'
    # parse parts of paths; calculate modules
    g_stem, g_mods, _ = gold_parts
    if input_length == 2:
        i_stem, _ = input_parts
        if i_stem == g_stem:
            for m in g_mods.split('_'):
                modules.append(m)
    if input_length == 3:
        i_stem, i_mods, _ = input_parts
        if i_stem == g_stem and len(g_mods) > len(i_mods) and g_mods.startswith(i_mods):
            for m in g_mods[len(i_mods)+1:].split('_'):
                modules.append(m)
    return modules


def generate_cases(mode: str) -> list:
    """Return list of (input, output, gold) filename triplets.
    """
    tests_dir = Path('./tests')
    inp_files = list(tests_dir.glob('input/*'))
    gold_files = list(tests_dir.glob('gold/*'))
    cases = []
    for i in inp_files:
        for g in gold_files:
            modules = get_modules(i, g)
            if modules:
                cases.append(Case(i, g, modules, Path(OUTDIR, f'{mode}_{g.name}')))
    return cases


def test_lib() -> None:
    from ..main import build_pipeline, jnius_config, tools, presets
    cases = generate_cases('lib')
    for case in cases:
        used_tools = case.modules
        with open(case.input_path) as inp, open(case.output_path, 'w') as out:
            input_data = iter(inp.readlines())
            out.writelines(build_pipeline(input_data, used_tools, tools, presets, conll_comments=True))
        with open(case.gold_path) as gold, open(case.output_path) as out:
            gold_text = gold.read()
            out_text = out.read()
            assert gold_text == out_text, f'{case.output_path} is not equal {case.gold_path}'


# def test_cli():
#     assert True
#     pass


if __name__ == '__main__':
    test_lib()

# print(OUTDIR)
# rmtree(OUTDIR)
