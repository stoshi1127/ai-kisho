@echo off
:: start.bat

:: 仮想環境の有効化
call venv\Scripts\activate

:: 必要なディレクトリの作成
if not exist data mkdir data
if not exist outputs mkdir outputs
if not exist logs mkdir logs
if not exist templates mkdir templates

:: アプリケーションの起動
python app.py