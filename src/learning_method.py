# learning_method.py

def generate_study_plan(knowledge):
    """
    根据传入的知识点生成学习计划
    :param knowledge: 知识点的相关信息
    :return: 学习计划（字符串形式）
    """
    study_plan = f"针对 {knowledge} 的学习计划：\n"
    study_plan += "- 阅读相关资料\n"
    study_plan += "- 完成练习题\n"
    study_plan += "- 进行实践应用\n"
    return study_plan

# 这里添加一段示例代码，测试 generate_study_plan 函数
if __name__ == "__main__":
    # 测试函数
    knowledge = "Python 编程"
    print(generate_study_plan(knowledge))
