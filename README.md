# Daily Flower Slack Bot

毎日朝に花の情報をSlackに投稿するPythonボットです。平日（土日と祝日を除く）に自動実行されます。

## 機能

- 📅 平日のみ実行（土日と祝日を除外）
- 🌸 365日分の花の名前と花言葉をCSVから取得
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

`env.example`を参考に`.env`ファイルを作成してください：

```bash
cp env.example .env
```

`.env`ファイルに以下の値を設定：

```env
# Slack Webhook URL
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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
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

## トラブルシューティング

1. **環境変数が設定されていない**
   - `.env`ファイルが正しく設定されているか確認
   - GitHub Secretsが設定されているか確認

2. **Slackに投稿されない**
   - Webhook URLが正しいか確認
   - Slackアプリの権限設定を確認

### ログの確認

スクリプトは詳細なログを出力します。エラーが発生した場合はログを確認してください。

## ライセンス

MIT License

## 貢献

プルリクエストやイシューの報告を歓迎します！ 