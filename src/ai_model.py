import openai
import os

# 从环境变量中获取 OpenAI API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_related_knowledge(knowledge_point):
    """调用 OpenAI API 获取相关知识点信息"""
    prompt = f"请整理以下知识点的相关知识，并用简洁的语言描述：{knowledge_point}"
    try:
        response = openai.Completion.create(
            engine="gpt-4o-mini",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"调用 OpenAI API 出错: {e}"
