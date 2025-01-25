import os
import json
import sys
import time
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

RECORDS_DIR = Path("learning_progress")
RECORDS_DIR.mkdir(exist_ok=True)

class SpacedRepetitionSystem:
    def __init__(self):
        self.card_data = {}
    
    def update_card(self, card_id, quality):
        now = datetime.now()
        data = self.card_data.get(card_id, {
            'interval': 1,
            'repetitions': 0,
            'efactor': 2.5,
            'next_review': now
        })

        if quality < 3:
            data['interval'] = 1
            data['repetitions'] = 0
        else:
            if data['repetitions'] == 0:
                data['interval'] = 1
            elif data['repetitions'] == 1:
                data['interval'] = 6
            else:
                data['interval'] = int(data['interval'] * data['efactor'])
            
            data['efactor'] = max(1.3, data['efactor'] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
            data['repetitions'] += 1

        data['next_review'] = now + timedelta(days=data['interval'])
        self.card_data[card_id] = data
        return data

class LearningSession:
    def __init__(self, topic):
        self.topic = topic
        self.srs = SpacedRepetitionSystem()
        self.cards = []
        self.active = True
        self.save_file = RECORDS_DIR / f"{topic}.json"
        
        if self.save_file.exists():
            self.load_progress()

    def add_card(self, card):
        """改进的卡片添加方法"""
        # 确保card_id是整数
        card_id = int(card['id'])
        
        # 初始化卡片数据如果不存在
        if card_id not in self.srs.card_data:
            self.srs.card_data[card_id] = {
                'interval': 1,
                'repetitions': 0,
                'efactor': 2.5,
                'next_review': datetime.now()
            }
        
        # 避免重复添加卡片
        if not any(c['id'] == card_id for c in self.cards):
            self.cards.append({
                'id': card_id,
                'title': card['title'],
                'knowledge': card['knowledge'],
                'questions': card['questions']
            })

    def get_next_card(self):
        """改进的获取方法，带空值检查"""
        due_cards = []
        for card in self.cards:
            card_id = int(card['id'])
            if card_id in self.srs.card_data:
                srs_data = self.srs.card_data[card_id]
                if datetime.now() >= srs_data['next_review']:
                    due_cards.append((card, srs_data))
        
        due_cards.sort(key=lambda x: (x[1]['efactor'], x[1]['next_review']))
        return due_cards[0][0] if due_cards else None

    def save_progress(self):
        progress = {
            'topic': self.topic,
            'cards': self.cards,
            'srs_data': {
                int(k): v for k, v in self.srs.card_data.items()
            },
            'timestamp': datetime.now().isoformat()
        }
        with open(self.save_file, 'w') as f:
            json.dump(progress, f, default=str, indent=2)

    def load_progress(self):
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
                self.srs.card_data = {
                    int(k): {
                        **v,
                        'next_review': datetime.fromisoformat(v['next_review'])
                    } for k, v in data['srs_data'].items()
                }
                self.cards = data['cards']
        except Exception as e:
            print(f"⚠️  加载进度失败：{str(e)}")
            self.cards = []

def input_with_escape(prompt):
    try:
        import msvcrt
        print(prompt, end='', flush=True)
        input_str = []
        while True:
            char = msvcrt.getwch()
            if char == '\x1b':
                print("\n⚠️  正在保存进度并退出...")
                return None
            elif char == '\r':
                print()
                return ''.join(input_str)
            elif char == '\x08':
                if input_str:
                    input_str.pop()
                    sys.stdout.write('\b \b')
            else:
                input_str.append(char)
                sys.stdout.write(char)
            sys.stdout.flush()
    except ImportError:
        print(prompt, end='', flush=True)
        input_str = []
        while True:
            char = sys.stdin.read(1)
            if char == '\x1b':
                print("\n⚠️  正在保存进度并退出...")
                return None
            elif char == '\n':
                return ''.join(input_str)
            elif char == '\x7f':
                if input_str:
                    input_str.pop()
                    sys.stdout.write('\b \b')
            else:
                input_str.append(char)
                sys.stdout.write(char)
            sys.stdout.flush()

def conduct_learning(client, session):
    while session.active:
        try:
            current_card = session.get_next_card()
            if not current_card:
                print("\n🎉 所有知识点已达标！")
                session.save_file.unlink()
                return

            print(f"\n📘 当前知识点：{current_card['title']}")
            print("="*60)
            print(current_card['knowledge'])
            
            user_input = input_with_escape("\n↵ 按 Enter 开始练习（ESC退出）: ")
            if user_input is None:
                session.active = False
                return

            scores = []
            for i, qa in enumerate(current_card['questions'], 1):
                print(f"\n❓ 问题 {i}: {qa['q']}")
                user_input = input_with_escape("   输入答案或按 Enter 查看参考答案（ESC退出）: ")
                if user_input is None:
                    session.active = False
                    return
                
                print(f"💡 参考答案: {qa['a']}")
                while True:
                    try:
                        score_input = input_with_escape("请评分（1-困难 3-一般 5-简单，ESC退出）: ")
                        if score_input is None:
                            session.active = False
                            return
                        score = int(score_input)
                        if 1 <= score <= 5:
                            scores.append(score)
                            break
                        print("请输入1-5之间的数字！")
                    except ValueError:
                        print("请输入有效数字！")

            avg_score = sum(scores) / len(scores)
            session.srs.update_card(int(current_card['id']), avg_score)
            session.save_progress()
        
        except Exception as e:
            print(f"⚠️  学习流程异常：{str(e)}")
            session.save_progress()
            break

def main():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    while True:
        try:
            print("\n" + "="*40)
            topic = input_with_escape("请输入学习主题（ESC退出程序）: ")
            if topic is None:
                print("\n👋 再见！")
                break
            if not topic.strip():
                print("⚠️  主题不能为空！")
                continue

            session = LearningSession(topic.strip())
            
            if not session.cards:
                print("🔄 正在生成学习内容...")
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{
                            "role": "system",
                            "content": """你是一个严格遵循JSON格式的课程生成器，请按以下模板生成内容：
{
    "cards": [
        {
            "id": 唯一数字ID（必须为整数）,
            "title": "卡片标题",
            "knowledge": "知识点说明（100字内）",
            "questions": [
                {"q": "基础概念问题", "a": "参考答案"},
                {"q": "应用场景问题", "a": "参考答案"}
            ]
        }
    ]
}"""
                        }, {
                            "role": "user",
                            "content": f"请为【{topic}】生成3-5张结构严格的学习卡片"
                        }],
                        temperature=0.3,
                        response_format={"type": "json_object"},
                        max_tokens=2000
                    )

                    try:
                        response_data = json.loads(response.choices[0].message.content)
                        if "cards" not in response_data:
                            raise KeyError("缺少cards字段")
                        
                        cards = response_data["cards"]
                        if len(cards) < 1:
                            raise ValueError("卡片数量不足")
                            
                        for card in cards:
                            # 强制转换ID为整数
                            card['id'] = int(card['id'])
                            session.add_card(card)
                        session.save_progress()

                    except (json.JSONDecodeError, KeyError, ValueError) as e:
                        print(f"❌ 内容生成失败：{str(e)}")
                        continue

                except Exception as e:
                    print(f"❌ API请求失败：{str(e)}")
                    continue

            conduct_learning(client, session)
            
        except KeyboardInterrupt:
            if 'session' in locals():
                session.save_progress()
            print("\n⚠️  已保存进度并安全退出")
            break

if __name__ == "__main__":
    main()