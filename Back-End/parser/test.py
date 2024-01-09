from AnalysisTable import AnalysisTable
from SpecFamily import SpecFamilyItem, SpecFamily
from Parser import Parser
from Grammar import GRAMMAR, GRAMMAR_WITH_EPSILON, NON_TERMINATOR, TERMINATOR

"""

spec_family = SpecFamily(grammar=GRAMMAR)
spec_family.insertExgrammar(0, "S_", ["S"])
spec_family.insertExgrammar(1, "S", ["B", "B"])
spec_family.insertExgrammar(2, "B", ["b", "B"])
spec_family.insertExgrammar(3, "B", ["a"])


# 创建第一个项目
spec_family_item_0 = SpecFamilyItem(state=0)
spec_family_item_0.insertContent("S_", ["^", "S"], ["$"])
spec_family_item_0.insertContent("S", ["^", "B", "B"], ["$"])
spec_family_item_0.insertContent("B", ["^", "S"], ["a", "b"])
spec_family_item_0.insertContent("B", ["^", "$"], ["a", "b"])
spec_family_item_0.insertTransfrom("S", 1)
spec_family_item_0.insertTransfrom("B", 2)
spec_family_item_0.insertTransfrom("b", 3)
spec_family_item_0.insertTransfrom("a", 4)
spec_family.insertSpecFamilyItem(spec_family_item_0)

# 创建第二个项目
spec_family_item_1 = SpecFamilyItem(state=1)
spec_family_item_1.insertContent("S_", ["S", "^"], ["$"])
spec_family.insertSpecFamilyItem(spec_family_item_1)

# 创建第三个项目
spec_family_item_2 = SpecFamilyItem(state=2)
spec_family_item_2.insertContent("S", ["B", "^", "B"], ["$"])
spec_family_item_2.insertContent("B", ["^", "b", "B"], ["$"])
spec_family_item_2.insertContent("B", ["^", "a"], ["$"])
spec_family_item_2.insertTransfrom("B", 5)
spec_family_item_2.insertTransfrom("b", 6)
spec_family_item_2.insertTransfrom("a", 7)
spec_family.insertSpecFamilyItem(spec_family_item_2)

# 创建第四个项目
spec_family_item_3 = SpecFamilyItem(state=3)
spec_family_item_3.insertContent("B", ["b", "^", "B"], ["b", "a"])
spec_family_item_3.insertContent("B", ["^", "b", "B"], ["b", "a"])
spec_family_item_3.insertContent("B", ["^", "a"], ["b", "a"])
spec_family_item_3.insertTransfrom("b", 3)
spec_family_item_3.insertTransfrom("B", 8)
spec_family_item_3.insertTransfrom("a", 4)
spec_family.insertSpecFamilyItem(spec_family_item_3)

# 创建第五个项目
spec_family_item_4 = SpecFamilyItem(state=4)
spec_family_item_4.insertContent("B", ["a", "^"], ["a", "b"])
spec_family.insertSpecFamilyItem(spec_family_item_4)

# 创建第六个项目
spec_family_item_5 = SpecFamilyItem(state=5)
spec_family_item_5.insertContent("S", ["B", "B", "^"], ["$"])
spec_family.insertSpecFamilyItem(spec_family_item_5)

# 创建第七个项目
spec_family_item_6 = SpecFamilyItem(state=6)
spec_family_item_6.insertContent("B", ["b", "^", "B"], ["$"])
spec_family_item_6.insertContent("B", ["^", "b", "B"], ["$"])
spec_family_item_6.insertContent("B", ["^", "a"], ["$"])
spec_family_item_6.insertTransfrom("a", 7)
spec_family_item_6.insertTransfrom("b", 6)
spec_family_item_6.insertTransfrom("B", 9)
spec_family.insertSpecFamilyItem(spec_family_item_6)

# 创建第八个项目
spec_family_item_7 = SpecFamilyItem(state=7)
spec_family_item_7.insertContent("B", ["a", "^"], ["$"])
spec_family.insertSpecFamilyItem(spec_family_item_7)

# 创建第九个项目
spec_family_item_8 = SpecFamilyItem(state=8)
spec_family_item_8.insertContent("B", ["b", "B", "^"], ["a", "b"])
spec_family.insertSpecFamilyItem(spec_family_item_8)

# 创建第十个项目
spec_family_item_9 = SpecFamilyItem(state=9)
spec_family_item_9.insertContent("B", ["b", "B", "^"], ["$"])
spec_family.insertSpecFamilyItem(spec_family_item_9)

"""


def main():
    spec_family = SpecFamily(GRAMMAR, NON_TERMINATOR)
    analysis_table = AnalysisTable(spec_family, TERMINATOR, NON_TERMINATOR)
    analysis_table.to_excel('output.xlsx')


main()
