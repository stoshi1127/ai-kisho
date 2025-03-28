# prompt_engine.py
import json
import os

class PromptEngine:
    def __init__(self):
        # 五感表現データベースの読み込み
        self.sense_db = self._load_sense_database()
        # 行動喚起フレーズの読み込み
        self.action_phrases = self._load_action_phrases()
        # 料理ジャンルテンプレートの読み込み
        self.cuisine_templates = self._load_cuisine_templates()
    
    def _load_sense_database(self):
        """五感表現データベースを読み込む"""
        try:
            with open('data/sense_database.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # ファイルがない場合は空の辞書を返す
            return {
                "visual": [], "audio": [], 
                "taste": [], "smell": [], "touch": []
            }
    
    def _load_action_phrases(self):
        """行動喚起フレーズを読み込む"""
        try:
            with open('data/action_phrases.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "awareness": [], "interest": [],
                "desire": [], "action": []
            }
    
    def _load_cuisine_templates(self):
        """料理ジャンルテンプレートを読み込む"""
        try:
            with open('data/cuisine_templates.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def create_prompt(self, shop_info, platform, purpose):
        """
        プロンプトを生成する
        
        params:
        - shop_info: 店舗情報の辞書
        - platform: 'blog', 'sns', 'google'のいずれか
        - purpose: 'awareness', 'reservation', 'visit'のいずれか
        
        returns:
        - 完成したプロンプト
        """
        # 基本プロンプトの作成
        base_prompt = self._create_base_prompt(shop_info)
        
        # プラットフォーム別プロンプトの追加
        if platform == 'blog':
            platform_prompt = self._create_blog_prompt()
        elif platform == 'sns':
            platform_prompt = self._create_sns_prompt()
        elif platform == 'google':
            platform_prompt = self._create_google_prompt()
        else:
            platform_prompt = ""
        
        # 行動喚起段階の設定
        action_prompt = self._create_action_prompt(purpose)
        
        # 料理ジャンル特化プロンプトの追加
        cuisine_type = shop_info.get('cuisine_type', 'general')
        cuisine_prompt = self._get_cuisine_prompt(cuisine_type)
        
        # 五感表現ガイドラインの追加
        sense_prompt = self._create_sense_prompt()
        
        # 最終プロンプトの組み立て
        full_prompt = f"{base_prompt}\n\n{platform_prompt}\n\n{action_prompt}\n\n{cuisine_prompt}\n\n{sense_prompt}"
        
        return full_prompt
    
    def _create_base_prompt(self, shop_info):
        """基本プロンプトを作成する"""
        return f"""
# 飲食店記事作成プロンプト

## 店舗情報
店舗名: {shop_info.get('name', '')}
料理ジャンル: {shop_info.get('cuisine_type', '')}
地域: {shop_info.get('location', '')}
ターゲット顧客層: {shop_info.get('target_customers', '')}
価格帯: {shop_info.get('price_range', '')}
店舗の特徴: {shop_info.get('features', '')}

## 推しメニュー情報
{self._format_menu_items(shop_info.get('menu_items', []))}

## こだわりポイント
食材: {shop_info.get('ingredients_focus', '')}
調理法: {shop_info.get('cooking_method', '')}
雰囲気: {shop_info.get('atmosphere', '')}
サービス: {shop_info.get('service', '')}
        """
    
    def _format_menu_items(self, menu_items):
        """メニュー項目をフォーマットする"""
        if not menu_items:
            return "情報なし"
        
        result = ""
        for i, item in enumerate(menu_items, 1):
            name = item.get('name', '')
            price = item.get('price', '')
            features = item.get('features', '')
            result += f"メニュー{i}: {name}, {price}, {features}\n"
        
        return result
    
    def _create_blog_prompt(self):
        """ブログ記事用プロンプトを作成する"""
        return """
## ブログ記事構成
- タイトル: SEO効果の高い魅力的なタイトル（30字以内）
- 導入部: 読者の興味を引く導入（200-300字）
- 本文セクション1: [推しメニューの魅力]（400-500字）
- 本文セクション2: [こだわりポイント]（400-500字）
- 本文セクション3: [おすすめの楽しみ方/時間帯/組み合わせ]（400-500字）
- 本文セクション4: [季節限定/イベント情報]（必要に応じて）（300-400字）
- まとめ: 行動喚起を含む結び（200-300字）

## SEO最適化指示
- H1タグにメインキーワード（地域名+料理ジャンル+特徴）を含める
- H2タグは各セクションのタイトルとして使用し、関連キーワードを含める
- 本文中に関連キーワードを自然な形で5-7回使用
- メタディスクリプション案も作成（120字以内）
        """
    
    def _create_sns_prompt(self):
        """SNS投稿用プロンプトを作成する"""
        return """
## SNS投稿構成
- キャッチコピー: 注目を集める短いフレーズ（15字以内）
- 本文: 五感を刺激し行動を促す魅力的な文章（300-400字）
- ハッシュタグ: 関連性の高いハッシュタグ15-20個
- ストーリーズ用テキスト: 3パターン（各20字以内）
- コメント誘導質問: エンゲージメントを高める質問

## SNS最適化指示
- 最初の3行で読者の注意を引く内容にする
- 絵文字を適切に使用して視認性を高める
- 限定感や即時性を感じさせる表現を含める
- 画像キャプションとの相性を考慮する
        """
    
    def _create_google_prompt(self):
        """Googleビジネス投稿用プロンプトを作成する"""
        return """
## Googleビジネス投稿構成
- タイトル: 簡潔で検索意図に合致するタイトル（20字以内）
- 本文: 行動喚起を含む簡潔な説明（150-200字以内）
- アクションボタン: [予約する/詳細を見る/電話する/ルートを検索]から最適なものを選択
- 掲載期間: [〇日間]の期間設定推奨

## ローカルSEO最適化指示
- 地域名を自然な形で含める
- 店舗から半径2km以内の地名やランドマークに言及する
- 「近く」「徒歩〇分」などの位置表現を活用する
- 検索意図に合致する簡潔な表現を優先する
        """
    
    def _create_action_prompt(self, purpose):
        """行動喚起プロンプトを作成する"""
        action_stages = {
            'awareness': '認知段階：店舗・料理の魅力を五感で伝えることを重視してください。',
            'reservation': '予約促進：具体的な予約方法と予約するメリットを強調してください。',
            'visit': '来店促進：すぐに行動したくなるような緊急性と具体的な来店メリットを強調してください。'
        }
        
        return f"""
## 行動喚起設計
目的：{action_stages.get(purpose, action_stages['awareness'])}

- 認知段階: 店舗・料理の魅力を五感で伝える
- 興味段階: 他店との差別化ポイントを明確に
- 欲求段階: 「食べたい」「訪れたい」感情を喚起
- 行動段階: 具体的な予約・来店方法を案内
        """
    
    def _get_cuisine_prompt(self, cuisine_type):
        """料理ジャンル特化プロンプトを取得する"""
        # 料理ジャンルテンプレートから取得
        cuisine_template = self.cuisine_templates.get(cuisine_type, self.cuisine_templates.get('general', ''))
        return f"""
## 料理ジャンル特化指示
{cuisine_template}
        """
    
    def _create_sense_prompt(self):
        """五感表現ガイドラインを作成する"""
        return """
## 記事作成条件
- 五感表現（視覚、聴覚、味覚、嗅覚、触覚）をバランスよく使用すること
- 行動喚起要素を3箇所に自然に配置すること
- 地域名と料理ジャンルに関連するキーワードを自然に組み込むこと
- 季節感を反映させること
- 店舗の差別化ポイントを強調すること

以上の情報に基づいて、五感表現豊かな魅力的な記事を作成してください。
        """