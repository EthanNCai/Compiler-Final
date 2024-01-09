"""
这是伪代码！这不是真的代码，仅供参考！
"""
#首先要导入下级目录的东西

"""
为了进行合理的测试，请务必看一下下面这段内容

因为词法分析器是PL0的，只能识别PL0的记号流，所以对于我们的ab的那个简单测试文法（下面我称其为ab文法）词法分析器不能识别
但是为了继续编程下去，我们需要一点技巧。

我现在规定： a 这个 bb文法中的非终结符现在 对应着 PL0 中的     if关键字         token为（22）
           b 这个 bb文法中的非终结符现在对应着 PL0 中的      var关键字      token为（21）
            也就是，比如我想测试输入 bb 这个bb文法中的句子，那么，实际的测试记事本里应该写 var var
            比如我想测试输入 aa 这个bb文法中的句子，那么，实际的测试记事本里应该写 if if 
            比如我想测试输入 ab 这个bb文法中的句子，那么，实际的测试记事本里应该写 if var
            
            
然后，现在考虑token流转非终结符流的翻译器的原理，实际上就是建立一个映射：

    假设translator是一个函数的话，有：
    对于上面那个例子运行 translator(22) 应该返回一个 a
    运行              translator(21) 应该返回一个 b 
    
    这样你就可以把token流转换为非终结符流了（这个translator不能是一个字典，因为PL0中的变量
    名可以是多样的，比如说 nice 和 name 这种变量名都会映射到 ID 这个非终结符）
"""


"""
构建项目集规范族
"""

# spec_family = ?（涂哥还没写完，这个部分用test里面的那一大堆手动构建一个specFamily出来）

"""
构建分析表
"""
# analysis_table = AnalysisTable(spec_family)

"""
词法分析器分析
"""

# json_path = 'path/to/the/json/lexer.json'# 这个json路径可以随便指派，最好就在这级目录
# lexer = Lexer('path/to/the/file',json_path)


"""
语法分析器
"""
# parser = Parser(analysis_table,json_path)
# 这个Parser就是AnalysisStack，记得改一下名！