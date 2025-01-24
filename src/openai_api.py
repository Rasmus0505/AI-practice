import os
from openai import OpenAI

# 从环境变量中获取 OpenAI API 密钥
api_key = os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key)

def get_related_knowledge(query):
    """
    调用 OpenAI GPT-4o-mini 模型生成学习内容
    """
    try:
        # 调用 Chat Completion 接口
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
            model="gpt-4o-mini",  # 模型名称
        )
        # 返回生成结果
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"调用 OpenAI API 出错: {e}")
        return None

if __name__ == "__main__":
    query = "什么是货币金融学？"  # 测试输入
    result = get_related_knowledge(query)
    if result:
        print("AI 返回的结果:")
        print(result)
    else:
        print("AI 没有返回任何结果，请检查 API 配置或输入内容。")
