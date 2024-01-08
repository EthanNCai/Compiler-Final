from SpecFamily import SpecFamily, SpecFamilyItem


GRAMMAR = {
    'S_': (['S'],),
    'S': (['B', 'B']),
    'B': (['b', 'B'], ['a'],),
}


spec_family = SpecFamily(grammar=GRAMMAR)
spec_family.insertIndexList(0, "S_", ["S"])
spec_family.insertIndexList(1, "S", ["B", "B"])
spec_family.insertIndexList(2, "B", ["b", "B"])
spec_family.insertIndexList(3, "B", ["a"])

spec_family_0 = SpecFamilyItem(state=0)
spec_family_0.insertContent("S_", ["^", "S"], ["$"])
spec_family_0.insertContent("S", ["^", "B", "B"], ["$"])
spec_family_0.insertContent("B", ["^", "S"], ["a", "b"])
spec_family_0.insertContent("B", ["^", "$"], ["a", "b"])
spec_family_0.insertTransfrom("S", 1)
spec_family_0.insertTransfrom("B", 2)
spec_family_0.insertTransfrom("b", 3)
spec_family_0.insertTransfrom("a", 4)
