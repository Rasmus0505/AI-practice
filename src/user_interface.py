# user_interface.py

def get_user_input():
    """
    获取用户输入的知识点
    :return: 用户输入的字符串（知识点）
    """
    knowledge_point = input("请输入你想学习的知识点：")
    return knowledge_point

def display_output(related_knowledge, study_plan):
    """
    显示学习结果
    :param related_knowledge: 获取的相关知识
    :param study_plan: 生成的学习计划
    """
    print(f"\n相关知识点：{related_knowledge}")
    print(f"\n学习计划：{study_plan}")

# 在此添加执行代码块进行测试
if __name__ == "__main__":
    # 模拟获取用户输入
    knowledge_point = get_user_input()
    
    # 假设获取到的相关知识和学习计划
    related_knowledge = f"与 '{knowledge_point}' 相关的知识"
    study_plan = f"1. 学习 '{knowledge_point}' 基础\n2. 完成相关练习\n3. 复习"
    
    # 显示输出
    display_output(related_knowledge, study_plan)
