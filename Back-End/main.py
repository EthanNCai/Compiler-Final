"""
这是伪代码！这不是真的代码，仅供参考！
"""
#首先要导入下级目录的东西

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