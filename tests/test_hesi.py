import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run import costs, factor

def test_size_factor():
    assert np.allclose(factor(np.arange(1,9)),[1.20,1.10,1.05,1,0.95,0.95,0.90,0.90])

def test_usda_exact_boundary_values():
    ages=np.array([0,1,3,5,8,11,12,13,14,18,19,20,50,51,70,71])
    male=np.ones(len(ages),dtype=int)
    thrifty=[110.7,110.7,166.5,181.6,201.7,233.2,249.3,249.3,314.5,314.5,314.5,307.4,307.4,272.3,272.3,259.9]
    low=[157.7,157.7,164.4,171,245.2,258.1,301.4,301.4,307.1,307.1,303.6,303.6,303.6,285.4,285.4,283.6]
    assert np.allclose(costs(ages,male,'thrifty'),thrifty)
    assert np.allclose(costs(ages,male,'low'),low)
    assert costs(np.array([19]),np.array([1]),'low')[0]==303.6
    assert costs(np.array([19]),np.array([1]),'thrifty')[0]==314.5

def test_female_adult_boundaries():
    ages=np.array([18,19,20,50,51,70,71])
    f=np.full(len(ages),2)
    assert np.allclose(costs(ages,f,'thrifty'),[250.1,250.1,245.6,245.6,228.6,228.6,251.4])
    assert np.allclose(costs(ages,f,'low'),[258.7,263.7,263.7,263.7,256.6,256.6,256.6])
