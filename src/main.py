import os
import openai

# 从环境变量中获取 OpenAI API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_personalized_study_plan(learning_goal, learning_style, time_limit):
    # 根据用户的学习目标、学习风格和时间限制等因素，生成个性化的学习计划
    prompt = f"根据学习目标{learning_goal}、学习风格{learning_style}和时间限制{time_limit}，生成个性化的学习计划。"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )
    study_plan = response.choices[0].text.strip()
    return study_plan

def main():
    # 获取用户输入的学习目标、学习风格和时间限制等信息
    learning_goal = input("请输入您的学习目标：")
    learning_style = input("请输入您的学习风格：")
    time_limit = input("请输入您的时间限制：")
    
    # 生成个性化的学习计划
    study_plan = generate_personalized_study_plan(learning_goal, learning_style, time_limit)
    
    # 输出学习计划
    print("个性化学习计划：")
    print(study_plan)

if __name__ == "__main__":
    main()
