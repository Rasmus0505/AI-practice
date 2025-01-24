import os
from openai import OpenAI

# 从环境变量中获取 OpenAI API 密钥
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_personalized_study_plan(learning_goal, learning_style, time_limit):
    # 根据用户的学习目标、学习风格和时间限制等因素，生成个性化的学习计划
    prompt = f"根据学习目标{learning_goal}、学习风格{learning_style}和时间限制{time_limit}，生成个性化的学习计划。"
    try:
        # 使用 ChatCompletion 接口
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        study_plan = response.choices[0].message.content.strip()
        return study_plan
    except Exception as e:
        print(f"调用 OpenAI API 出错: {e}")
        return None

def main():
    # 获取用户输入的学习目标、学习风格和时间限制等信息
    learning_goal = input("请输入您的学习目标：")
    learning_style = input("请输入您的学习风格：")
    time_limit = input("请输入您的时间限制：")
    
    # 生成个性化的学习计划
    study_plan = generate_personalized_study_plan(learning_goal, learning_style, time_limit)
    
    # 输出学习计划
    if study_plan:
        print("个性化学习计划：")
        print(study_plan)
    else:
        print("生成学习计划失败，请检查输入或API配置。")

if __name__ == "__main__":
    main()