"""Normative HESI bedroom rule for resolved household counts. NOT a HUD occupancy rule."""
from math import ceil

class UnresolvedComposition(ValueError):
    pass

def required_bedrooms(adults:int, children_under_18:int, identified_disjoint_couples:int=0)->int:
    """One room per adult except each identified adult couple shares one; max two children per room.
    Couples MUST be distinct pairs of adults (no individual in multiple pairs).
    Accessibility/disability accommodation needs are outside this baseline and flagged separately.
    """
    for name, value in [('adults',adults),('children_under_18',children_under_18),('identified_disjoint_couples',identified_disjoint_couples)]:
        if type(value) is not int or value < 0:
            raise UnresolvedComposition(f'{name} must be nonnegative integer')
    if adults < 1:
        raise UnresolvedComposition('At least one adult needed for baseline household model')
    if 2 * identified_disjoint_couples > adults:
        raise UnresolvedComposition('Overlapping/invalid couple assignments')
    return adults-identified_disjoint_couples+ceil(children_under_18/2)

def hud_eligible_bedroom_count(adults:int,children_under_18:int,identified_disjoint_couples:int=0)->int:
    n=required_bedrooms(adults,children_under_18,identified_disjoint_couples)
    if n>4:
        raise UnresolvedComposition('Household requires >4 bedrooms; excluded, never capped')
    return n
