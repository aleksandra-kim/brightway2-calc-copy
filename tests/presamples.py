# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from eight import *

from .fixtures.presamples_basic import write_database, basedir
from bw2calc.errors import OutsideTechnosphere, NonsquareTechnosphere
from bw2calc import (
    ComparativeMonteCarlo,
    LCA,
    MonteCarloLCA,
    ParameterVectorLCA,
)
from bw2data import *
from bw2data.tests import bw2test
from bw2data.utils import TYPE_DICTIONARY
import numpy as np
import pytest
import os


@pytest.fixture
@bw2test
def basic():
    write_database()


def test_writing_test_fixture(basic):
    assert len(databases) == 2
    assert len(methods) == 1

def test_fixture_lca_results(basic):
    expected = np.array([
        [       2/3,       4/15,  2/30],
        [-(2 + 2/3),      14/15, -4/15],
        [-(3 + 1/3),    2 + 2/3,   2/3]
    ])

def test_single_sample_presamples(basic):
    ss = os.path.join(basedir, "single-sample")

    lca = LCA({("test", "2"): 1}, method=("m",))
    lca.lci()
    assert np.allclose(
        lca.supply_array,
        np.array([-(2 + 2/3),      14/15, -4/15])
    )
    lca = LCA({("test", "2"): 1}, method=("m",), presamples=[ss])
    lca.lci()
    assert np.allclose(
        lca.supply_array,
        np.array([2, 1.4, 0.2])
    )

    mc = MonteCarloLCA({("test", "2"): 1}, method=("m",))
    next(mc)
    assert np.allclose(
        mc.supply_array,
        np.array([-(2 + 2/3),      14/15, -4/15])
    )
    mc = MonteCarloLCA({("test", "2"): 1}, method=("m",), presamples=[ss])
    next(mc)
    assert np.allclose(
        mc.supply_array,
        np.array([2, 1.4, 0.2])
    )

    mc = ParameterVectorLCA({("test", "2"): 1}, method=("m",))
    next(mc)
    assert mc.technosphere_matrix[
        mc.product_dict[("test", "2")],
        mc.activity_dict[("test", "2")],
    ] == 0.5
    mc = ParameterVectorLCA({("test", "2"): 1}, method=("m",), presamples=[ss])
    next(mc)
    assert mc.technosphere_matrix[
        mc.product_dict[("test", "2")],
        mc.activity_dict[("test", "2")],
    ] == 1

    mc = ComparativeMonteCarlo([{("test", "2"): 1}], method=("m",))
    next(mc)
    assert mc.technosphere_matrix[
        mc.product_dict[("test", "2")],
        mc.activity_dict[("test", "2")],
    ] == 0.5
    mc = ComparativeMonteCarlo([{("test", "2"): 1}], method=("m",), presamples=[ss])
    next(mc)
    assert mc.technosphere_matrix[
        mc.product_dict[("test", "2")],
        mc.activity_dict[("test", "2")],
    ] == 1
