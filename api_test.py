# api_test.py
import openai
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    # 簡単なAPIリクエストでテスト (gpt-4 から gpt-3.5-turbo に変更)
    response = openai.ChatCompletion.create(
        model="gpt-4",  # ここを変更
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, world!"}
        ],
        max_tokens=50
    )
    print("API接続成功!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"API接続エラー: {e}")