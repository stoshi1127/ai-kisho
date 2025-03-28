#!/bin/bash
# start.sh

# 仮想環境の有効化
source venv/bin/activate

# 必要なディレクトリの作成
mkdir -p data
mkdir -p outputs
mkdir -p logs
mkdir -p templates

# アプリケーションの起動
python app.py