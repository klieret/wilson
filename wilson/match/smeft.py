"""Matcher from the SMEFT 'Warsaw up' basis to the WET JMS basis.

Based on arXiv:1908.05295."""


import numpy as np
from math import sqrt, pi
import wcxf
import wilson
from wilson.parameters import p as default_parameters
from wilson.util import smeftutil, wetutil
from wilson.match import smeft_tree


def match_all(d_SMEFT, parameters=None):
    """Match the SMEFT Warsaw basis onto the WET JMS basis."""
    p = default_parameters.copy()
    if parameters is not None:
        # if parameters are passed in, overwrite the default values
        p.update(parameters)
    C = wilson.util.smeftutil.wcxf2arrays_symmetrized(d_SMEFT)
    C_WET = smeft_tree.match_all_array(C, p)
    C_WET = wilson.translate.wet.rotate_down(C_WET, p)
    C_WET = wetutil.unscale_dict_wet(C_WET)
    d_WET = wilson.util.smeftutil.arrays2wcxf(C_WET)
    basis = wcxf.Basis['WET', 'JMS']
    keys = set(d_WET.keys()) & set(basis.all_wcs)
    d_WET = {k: d_WET[k] for k in keys}
    return d_WET
