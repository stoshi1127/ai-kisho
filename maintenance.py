# maintenance.py
import os
import json
import shutil
import logging
from datetime import datetime, timedelta

logging.basicConfig(
    filename=f'logs/maintenance_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def backup_data():
    """データベースのバックアップを作成"""
    backup_dir = f'backups/{datetime.now().strftime("%Y%m%d")}'
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        for filename in os.listdir('data'):
            shutil.copy(f'data/{filename}', f'{backup_dir}/{filename}')
        logger.info("データベースのバックアップを作成しました")
        return True
    except Exception as e:
        logger.error(f"バックアップの作成に失敗しました: {str(e)}")
        return False

def cleanup_logs():
    """古いログファイルを削除"""
    try:
        for filename in os.listdir('logs'):
            file_path = f'logs/{filename}'
            # 30日以上前のログを削除
            if os.path.isfile(file_path):
                creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if datetime.now() - creation_time > timedelta(days=30):
                    os.remove(file_path)
        logger.info("古いログファイルを削除しました")
        return True
    except Exception as e:
        logger.error(f"ログの削除に失敗しました: {str(e)}")
        return False

def cleanup_outputs():
    """古い出力ファイルを削除"""
    try:
        for filename in os.listdir('outputs'):
            file_path = f'outputs/{filename}'
            # 90日以上前の出力を削除
            if os.path.isfile(file_path):
                creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if datetime.now() - creation_time > timedelta(days=90):
                    os.remove(file_path)
        logger.info("古い出力ファイルを削除しました")
        return True
    except Exception as e:
        logger.error(f"出力ファイルの削除に失敗しました: {str(e)}")
        return False

def update_sense_database(new_expressions=None):
    """五感表現データベースを更新"""
    if not new_expressions:
        logger.info("新しい表現がないため、更新をスキップします")
        return True
    
    try:
        with open('data/sense_database.json', 'r', encoding='utf-8') as f:
            sense_db = json.load(f)
        
        # 新しい表現を追加
        for sense_type, expressions in new_expressions.items():
            if sense_type in sense_db:
                for expr in expressions:
                    if expr not in sense_db[sense_type]:
                        sense_db[sense_type].append(expr)
        
        with open('data/sense_database.json', 'w', encoding='utf-8') as f:
            json.dump(sense_db, f, ensure_ascii=False, indent=4)
        
        logger.info("五感表現データベースを更新しました")
        return True
    except Exception as e:
        logger.error(f"五感表現データベースの更新に失敗しました: {str(e)}")
        return False

if __name__ == "__main__":
    backup_data()
    cleanup_logs()
    cleanup_outputs()
    # 必要に応じて新しい表現を追加
    # update_sense_database({
    #     "visual": ["新しい視覚表現"],
    #     "taste": ["新しい味覚表現"]
    # })
    logger.info("メンテナンスタスクが完了しました")