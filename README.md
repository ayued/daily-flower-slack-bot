# Daily Flower Slack Bot

毎朝、今日のお花をSlackに投稿するPythonボットです。

## 機能

- 📅 毎朝10時に実行（祝日を除外）
- 🌸 365日分の花の名前と花言葉をCSVから取得（日比谷花壇さんのサイトから引用させていただいています https://www.hibiyakadan.com/ext/hanakotoba）
- 💬 Slack Webhookでメッセージを投稿
- 🤖 GitHub Actionsで自動実行

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <your-repository-url>
cd daily-flower-slack-bot
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env`ファイルを作成し、以下の値を設定

```env
# Slack Webhook URL
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
```

### 4. Slack Webhookの設定

1. Slackワークスペースでアプリを作成
2. Incoming Webhooksを有効化
3. Webhook URLを取得して環境変数に設定

## 使い方

### ローカルでの実行

```bash
python flower_bot.py
```

### GitHub Actionsでの自動実行

1. GitHubリポジトリのSettings > Secrets and variables > Actionsで以下のシークレットを設定：
   - `SLACK_WEBHOOK_URL`

2. ワークフローは毎日朝9時（JST）に自動実行されます

## ファイル構成

daily-flower-slack-bot/
├── flower_bot.py          # メインスクリプト
├── flowers.csv            # 花のデータ（365日分）
├── requirements.txt       # Python依存関係
├── env.example           # 環境変数テンプレート
├── .github/workflows/    # GitHub Actions設定
│   └── daily_flower.yml
└── README.md             # このファイル

## 花のデータ

`flowers.csv`には365日分の花の名前と花言葉が含まれています。必要に応じて編集してください。

```csv
day,flower_name,meaning
1,福寿草,幸せと長寿
2,梅,高潔・忍耐
...
```

## カスタマイズ

### 実行時間の変更

`.github/workflows/daily_flower.yml`のcron式を編集：

```yaml
- cron: '0 0 * * 1-5'  # UTC 0:00 = JST 9:00, 月-金のみ
```

### メッセージのカスタマイズ

`flower_bot.py`の`post_to_slack`メソッドを編集してメッセージ形式を変更できます。

## ライセンス

MIT License
