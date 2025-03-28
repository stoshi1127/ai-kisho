# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
import logging
from datetime import datetime

from ai_engine import AIEngine
from prompt_engine import PromptEngine

# ロギングの設定
logging.basicConfig(
    filename=f'logs/app_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # クロスオリジン要求を許可

# AIエンジンとプロンプトエンジンのインスタンス化
ai_engine = AIEngine()
prompt_engine = PromptEngine()

@app.route('/')
def index():
    """トップページを表示"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    """記事を生成するAPI"""
    try:
        data = request.json
        shop_info = data.get('shop_info', {})
        platform = data.get('platform', 'blog')
        purpose = data.get('purpose', 'awareness')
        
        # プロンプトの生成
        prompt = prompt_engine.create_prompt(shop_info, platform, purpose)
        
        # 記事の生成
        content = ai_engine.generate_content(prompt)
        
        if not content:
            return jsonify({"error": "コンテンツの生成に失敗しました"}), 500
        
        # 生成した記事を保存
        output_filename = f"outputs/{shop_info.get('name', 'shop')}_{platform}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            "content": content,
            "prompt": prompt,
            "filename": output_filename
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"エラーが発生しました: {str(e)}\n{error_details}")
        return jsonify({"error": str(e), "details": error_details}), 500

@app.route('/refine', methods=['POST'])
def refine_content():
    """記事を改善するAPI"""
    try:
        data = request.json
        original_content = data.get('original_content', '')
        feedback = data.get('feedback', '')
        
        # 記事の改善
        refined_content = ai_engine.refine_content(original_content, feedback)
        
        if not refined_content:
            return jsonify({"error": "コンテンツの改善に失敗しました"}), 500
        
        return jsonify({
            "content": refined_content
        })
    
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/templates', methods=['GET'])
def get_templates():
    """利用可能な料理ジャンルテンプレートを取得"""
    try:
        with open('data/cuisine_templates.json', 'r', encoding='utf-8') as f:
            templates = json.load(f)
        
        return jsonify({
            "templates": list(templates.keys())
        })
    
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)