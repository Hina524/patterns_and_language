# English Writing Assistant Web App

このWebアプリケーションは、英語の文章を過去形に変換し、文のタイプを分析し、テンプレート文章を生成する機能を提供します。

## セットアップ

1. 必要なパッケージをインストール:
```bash
pip install flask
```

## 起動方法

1. アプリケーションを起動:
```bash
python app.py
```

2. ブラウザで以下のURLにアクセス:
```
http://127.0.0.1:5000/
```

## 機能

- **Past tense converter**: 英語の文章を過去形に変換
- **文タイプ分析**: Simple、Compound、Complex文の判定
- **前置詞句抽出**: 文章内の前置詞句を識別
- **Template Sentence Generator**: 文章作成のためのテンプレート生成

## ファイル構成

- `app.py`: Flaskアプリケーションのメインファイル
- `templates/index.html`: HTMLテンプレート
- `script.js`: JavaScriptロジック
- `style.css`: スタイルシート