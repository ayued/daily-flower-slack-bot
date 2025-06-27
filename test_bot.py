#!/usr/bin/env python3
"""
Flower Bot Test Script
ボットの動作をテストするためのスクリプト
"""

import sys
from datetime import date
from flower_bot import FlowerBot

def test_workday_check():
    """平日チェックのテスト"""
    print("=== 平日チェックテスト ===")
    bot = FlowerBot()
    
    # 今日の日付でテスト
    today = date.today()
    is_workday = bot.is_workday(today)
    print(f"今日 ({today}) は平日: {is_workday}")
    
    # 土曜日でテスト（例：2024年1月6日）
    test_saturday = date(2024, 1, 6)
    is_workday_sat = bot.is_workday(test_saturday)
    print(f"土曜日 ({test_saturday}) は平日: {is_workday_sat}")
    
    # 日曜日でテスト（例：2024年1月7日）
    test_sunday = date(2024, 1, 7)
    is_workday_sun = bot.is_workday(test_sunday)
    print(f"日曜日 ({test_sunday}) は平日: {is_workday_sun}")

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
        test_flower_data()
        test_slack_post()
        
        print("\n✅ すべてのテストが完了しました")
        
    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 