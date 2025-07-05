#!/usr/bin/env python3
"""
Flower Bot Test Script
ボットの動作をテストするためのスクリプト
"""

import sys
from datetime import date
from flower_bot import FlowerBot

def test_workday_check():
    """投稿対象曜日チェックのテスト"""
    print("=== 投稿対象曜日チェックテスト ===")
    bot = FlowerBot()
    
    # 今日の日付でテスト（日本時間）
    today = bot.get_jst_date()
    is_workday = bot.is_workday(today)
    weekday_names = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
    print(f"今日（日本時間）({today}) は{weekday_names[today.weekday()]}: {is_workday}")
    
    # 月曜日でテスト（例：2024年1月1日）
    test_monday = date(2024, 1, 1)
    is_workday_mon = bot.is_workday(test_monday)
    print(f"月曜日 ({test_monday}) は投稿対象: {is_workday_mon}")
    
    # 火曜日でテスト（例：2024年1月2日）
    test_tuesday = date(2024, 1, 2)
    is_workday_tue = bot.is_workday(test_tuesday)
    print(f"火曜日 ({test_tuesday}) は投稿対象: {is_workday_tue}")
    
    # 水曜日でテスト（例：2024年1月3日）
    test_wednesday = date(2024, 1, 3)
    is_workday_wed = bot.is_workday(test_wednesday)
    print(f"水曜日 ({test_wednesday}) は投稿対象: {is_workday_wed}")
    
    # 金曜日でテスト（例：2024年1月5日）
    test_friday = date(2024, 1, 5)
    is_workday_fri = bot.is_workday(test_friday)
    print(f"金曜日 ({test_friday}) は投稿対象: {is_workday_fri}")

def test_flower_data():
    """花のデータ取得のテスト"""
    print("\n=== 花のデータ取得テスト ===")
    bot = FlowerBot()
    
    # 今日の花を取得
    flower_info = bot.get_todays_flower()
    if flower_info:
        print(f"今日の花: {flower_info['name']}")
        print(f"花言葉: {flower_info['meaning']}")
        print(f"年間通算日: {flower_info['day']}")
    else:
        print("花の情報を取得できませんでした")

def test_time_check():
    """時間チェックのテスト"""
    print("\n=== 時間チェックテスト ===")
    bot = FlowerBot()
    
    from datetime import datetime, timezone, timedelta
    
    # 現在時刻でテスト（日本時間）
    utc_now = datetime.now(timezone.utc)
    jst = timezone(timedelta(hours=9))
    now_jst = utc_now.astimezone(jst)
    is_correct_time = bot.is_correct_time(now_jst)
    print(f"現在時刻（日本時間）({now_jst.strftime('%H:%M')}) は投稿時間: {is_correct_time}")
    
    # 9時00分でテスト（日本時間）
    test_time_9am = now_jst.replace(hour=9, minute=0, second=0, microsecond=0)
    is_correct_time_9am = bot.is_correct_time(test_time_9am)
    print(f"9時00分（日本時間）({test_time_9am.strftime('%H:%M')}) は投稿時間: {is_correct_time_9am}")
    
    # 10時00分でテスト（日本時間）
    test_time_10am = now_jst.replace(hour=10, minute=0, second=0, microsecond=0)
    is_correct_time_10am = bot.is_correct_time(test_time_10am)
    print(f"10時00分（日本時間）({test_time_10am.strftime('%H:%M')}) は投稿時間: {is_correct_time_10am}")

def test_slack_post():
    """Slack投稿のテスト（実際には投稿しない）"""
    print("\n=== Slack投稿テスト（モック） ===")
    bot = FlowerBot()
    
    # テスト用の花情報
    test_flower_info = {
        'name': 'テスト花',
        'meaning': 'テストの花言葉',
        'day': 1
    }
    
    # 実際には投稿せず、メッセージ構造のみ確認
    print("投稿メッセージ構造:")
    print(f"- 花名: {test_flower_info['name']}")
    print(f"- 花言葉: {test_flower_info['meaning']}")

def main():
    """メインテスト関数"""
    print("🌺 Flower Bot テスト開始 🌺")
    
    try:
        test_workday_check()
        test_time_check()
        test_flower_data()
        test_slack_post()
        
        print("\n✅ すべてのテストが完了しました")
        
    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 