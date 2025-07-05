#!/usr/bin/env python3
"""
Daily Flower Slack Bot
毎日花の情報をSlackに投稿するボット
"""

import os
import sys
import requests
import pandas as pd
import jpholiday
from datetime import datetime, date, timezone, timedelta
from dotenv import load_dotenv
import logging
from typing import Optional, Dict, Any

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FlowerBot:
    def __init__(self):
        """FlowerBotの初期化"""
        load_dotenv()
        
        # 環境変数の読み込み
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        # 必須環境変数のチェック
        if not self.slack_webhook_url:
            raise ValueError("SLACK_WEBHOOK_URLが設定されていません")
        
        # 花のデータの読み込み
        self.flowers_df = self._load_flowers_data()
        
    def _load_flowers_data(self) -> pd.DataFrame:
        """花のデータをCSVファイルから読み込み"""
        try:
            df = pd.read_csv('flowers.csv')
            logger.info(f"花のデータを読み込みました: {len(df)}件")
            return df
        except FileNotFoundError:
            logger.error("flowers.csvファイルが見つかりません")
            sys.exit(1)
        except Exception as e:
            logger.error(f"花のデータの読み込みに失敗しました: {e}")
            sys.exit(1)
    
    def is_workday(self, check_date: Optional[date] = None) -> bool:
        """指定された曜日（月曜・火曜・金曜）かどうかをチェック"""
        if check_date is None:
            check_date = self.get_jst_date()  # 日本時間の今日の日付を取得
        
        # 曜日チェック（0=月曜日, 1=火曜日, 4=金曜日）
        allowed_weekdays = [0, 1, 4]  # 月曜・火曜・金曜
        if check_date.weekday() not in allowed_weekdays:
            weekday_names = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
            logger.info(f"{check_date}は{weekday_names[check_date.weekday()]}のため、投稿をスキップします")
            return False
        
        # 祝日チェック
        if jpholiday.is_holiday(check_date):
            holiday_name = jpholiday.is_holiday_name(check_date)
            logger.info(f"{check_date}は祝日です: {holiday_name}")
            return False
        
        logger.info(f"{check_date}は投稿対象日です")
        return True
    
    def is_correct_time(self, check_time: Optional[datetime] = None) -> bool:
        """投稿時間（9時）かどうかをチェック"""
        if check_time is None:
            # 日本時間で現在時刻を取得
            utc_now = datetime.now(timezone.utc)
            jst = timezone(timedelta(hours=9))
            check_time = utc_now.astimezone(jst)
        
        # 9時に投稿
        if check_time.hour == 9 and check_time.minute == 0:
            logger.info(f"{check_time.strftime('%H:%M')}は投稿時間です")
            return True
        
        logger.info(f"{check_time.strftime('%H:%M')}は投稿時間ではありません（投稿時間: 9:00）")
        return False
    
    def get_jst_date(self) -> date:
        """日本時間（JST）の今日の日付を取得"""
        # UTCからJST（+9時間）を計算
        utc_now = datetime.now(timezone.utc)
        jst = timezone(timedelta(hours=9))
        jst_now = utc_now.astimezone(jst)
        return jst_now.date()
    
    def get_todays_flower(self) -> Optional[Dict[str, Any]]:
        """今日の花の情報を取得"""
        today = self.get_jst_date()  # 日本時間の今日の日付を取得
        today_str = today.strftime('%m-%d')  # MM-DD形式に変換

        logger.info(f"日本時間の今日の日付: {today} ({today_str})")

        # 花のデータから該当する日を取得
        flower_data = self.flowers_df[self.flowers_df['date'] == today_str]

        if flower_data.empty:
            logger.error(f"日付 {today_str} の花のデータが見つかりません")
            return None

        flower_info = flower_data.iloc[0]
        return {
            'name': flower_info['flower_name'],
            'meaning': flower_info['meaning'],
            'day': today_str
        }
    
    def post_to_slack(self, flower_info: Dict[str, Any]) -> bool:
        """Slackに花の情報を投稿（画像なし）"""
        # slack_webhook_urlのNoneチェック
        if not self.slack_webhook_url:
            logger.error("SLACK_WEBHOOK_URLが設定されていません")
            return False
            
        # メッセージの作成
        message = {
            "text": f"[お花Bot] おはようございます！\n今日のお花は{flower_info['name']}、花言葉は「{flower_info['meaning']}」です。"
        }
        
        try:
            response = requests.post(
                self.slack_webhook_url,
                json=message,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f"Slackに投稿しました: {flower_info['name']}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Slack投稿中にエラーが発生しました: {e}")
            return False
    
    def run(self) -> None:
        """メイン処理を実行"""
        logger.info("花の投稿処理を開始します")
        
        # 投稿対象曜日チェック
        if not self.is_workday():
            logger.info("今日は投稿対象曜日ではないため、投稿をスキップします")
            return
        
        # 投稿時間チェック
        if not self.is_correct_time():
            logger.info("現在は投稿時間ではないため、投稿をスキップします")
            return
        
        # 今日の花の情報を取得
        flower_info = self.get_todays_flower()
        if not flower_info:
            logger.error("花の情報の取得に失敗しました")
            return
        
        # Slackに投稿
        success = self.post_to_slack(flower_info)
        
        if success:
            logger.info("花の投稿が完了しました")
        else:
            logger.error("花の投稿に失敗しました")

def main() -> None:
    """メイン関数"""
    try:
        bot = FlowerBot()
        bot.run()
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 