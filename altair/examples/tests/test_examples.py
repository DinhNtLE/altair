import os

import pytest

from .. import iter_examples, load_example, iter_examples_with_metadata
from ... import *


def remove_empty_fields(spec):
    """Remove empty entries from the spec"""
    return {k:v for k, v in spec.items() if v}


@pytest.mark.parametrize('example', iter_examples())
def test_json_examples_round_trip(example):
    """
    Test that Altair correctly round-trips JSON with to_dict() and to_altair()
    """
    filename, json_dict = example
    print(filename)

    v = Chart.from_dict(json_dict)
    v_dict = v.to_dict()
    assert v_dict == json_dict

    # TEST: add this test back
    # code generation discards empty function calls, and so we
    # filter these out before comparison
    # v2 = eval(v.to_altair())
    # assert v2.to_dict() == remove_empty_fields(json_dict)


def test_load_example():
    filename, spec = next(iter_examples())
    root, _ = os.path.splitext(filename)

    assert load_example(filename) == spec
    assert load_example(root) == spec


@pytest.mark.parametrize('D', iter_examples_with_metadata())
def test_metadata(D):
    expected_keys = {'spec', 'filename', 'category', 'name', 'title'}
    assert len(expected_keys - set(D.keys())) == 0
    assert 'data' in D['spec']
