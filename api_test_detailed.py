# test_gpt4o.py
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

def test_gpt4o_connection():
    """GPT-4o への接続をテストする"""
    print("GPT-4o 接続テストを開始します...")
    
    # 環境変数の読み込み
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("エラー: OPENAI_API_KEY が設定されていません。")
        print(".env ファイルに API キーを設定するか、環境変数として設定してください。")
        sys.exit(1)
    
    try:
        # OpenAI クライアントの初期化
        client = OpenAI(api_key=api_key)
        
        # テスト用のシンプルなプロンプト
        test_prompt = "飲食店向けの記事で使える五感表現を3つ挙げてください。"
        
        print("GPT-4o に問い合わせ中...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは飲食店向け記事専門のAI'記事匠'です。"},
                {"role": "user", "content": test_prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # レスポンスの取得
        content = response.choices[0].message.content
        
        print("\n接続成功！GPT-4o からの応答:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        print("\nモデル情報:")
        print(f"モデル名: {response.model}")
        print(f"プロンプトトークン: {response.usage.prompt_tokens}")
        print(f"完了トークン: {response.usage.completion_tokens}")
        print(f"合計トークン: {response.usage.total_tokens}")
        
        return True
    
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_gpt4o_connection()
    if success:
        print("\nテスト成功: GPT-4o と正常に接続できました。")
    else:
        print("\nテスト失敗: GPT-4o との接続に問題があります。")