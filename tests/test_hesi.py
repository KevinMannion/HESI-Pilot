import numpy as np
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import run.py functions
sys.path.append(str(Path(__file__).resolve().parent.parent))
from run import costs, factor

def test_household_size_multipliers():
    """Verify official USDA size economy multipliers."""
    assert factor(1) == 1.20
    assert factor(2) == 1.10
    assert factor(3) == 1.05
    assert factor(4) == 1.00
    assert factor(5) == 0.95
    assert factor(6) == 0.95
    assert factor(7) == 0.90

def test_thrifty_age_boundaries():
    """Verify cost assignments across critical age boundaries for Thrifty plan."""
    c0 = costs(np.array([0]), np.array([1]), 'thrifty')
    c1 = costs(np.array([1]), np.array([1]), 'thrifty')
    assert c0[0] == c1[0]  # Age 0 uses age 1 provisional assignment per methodology
    
    # Adult male vs female cost differentiation at age 30
    m_cost = costs(np.array([30]), np.array([1]), 'thrifty')
    f_cost = costs(np.array([30]), np.array([2]), 'thrifty')
    assert m_cost[0] > f_cost[0]

def test_low_cost_age_boundaries():
    """Verify Low-Cost plan age bands and adult male group assignment."""
    cost_19 = costs(np.array([19]), np.array([1]), 'low')
    assert not np.isnan(cost_19[0])
