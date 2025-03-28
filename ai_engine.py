# ai_engine.py - 最新SDKバージョン用
import os
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

class AIEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", 4000))
        self.temperature = float(os.getenv("TEMPERATURE", 0.7))
    
    def generate_content(self, prompt):
        """プロンプトに基づいて内容を生成"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたは飲食店向け記事専門のAI'記事匠'です。五感表現に特化し、行動喚起を効果的に組み込んだ記事を生成します。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return None
    
    def refine_content(self, original_content, feedback):
        """フィードバックに基づいて内容を改善"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたは飲食店向け記事専門のAI'記事匠'です。提供された内容をフィードバックに基づいて改善します。"},
                    {"role": "user", "content": f"元の内容:\n{original_content}\n\nフィードバック:\n{feedback}\n\n改善した内容を提供してください。"}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return None