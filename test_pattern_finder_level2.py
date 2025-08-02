#!/usr/bin/env python3
import requests
import json
from tabulate import tabulate

# テストケースの定義
test_cases = [
    {
        "id": 1,
        "texts": [
            "The cat sits on the mat.",
            "The dog sits on the floor."
        ],
        "comment": "Common pattern with determiner, noun, verb, preposition"
    },
    {
        "id": 2,
        "texts": [
            "She quickly runs to school.",
            "He quickly walks to work."
        ],
        "comment": "Pattern with adverb modifying verb"
    },
    {
        "id": 3,
        "texts": [
            "I love eating pizza and pasta.",
            "We love eating burgers and fries."
        ],
        "comment": "Pattern with gerund and coordinated nouns"
    },
    {
        "id": 4,
        "texts": [
            "The beautiful garden blooms in spring.",
            "The beautiful park shines in summer."
        ],
        "comment": "Pattern with adjective-noun combination"
    },
    {
        "id": 5,
        "texts": [
            "Can you help me with this?",
            "Can you assist me with that?"
        ],
        "comment": "Modal auxiliary pattern"
    },
    {
        "id": 6,
        "texts": [
            "She has been studying all day.",
            "He has been working all night."
        ],
        "comment": "Present perfect continuous pattern"
    },
    {
        "id": 7,
        "texts": [
            "If it rains, we will stay home.",
            "If it snows, we will stay inside."
        ],
        "comment": "Conditional sentence pattern"
    },
    {
        "id": 8,
        "texts": [
            "The book that I read was interesting.",
            "The movie that I watched was boring."
        ],
        "comment": "Relative clause pattern"
    },
    {
        "id": 9,
        "texts": [
            "Running is good for health.",
            "Swimming is good for fitness."
        ],
        "comment": "Gerund as subject pattern"
    },
    {
        "id": 10,
        "texts": [
            "She told me to wait here.",
            "He asked me to wait there."
        ],
        "comment": "Infinitive phrase pattern"
    },
    {
        "id": 11,
        "texts": [
            "Not only did she sing, but she also danced.",
            "Not only did he play, but he also coached."
        ],
        "comment": "Complex correlative conjunction pattern"
    },
    {
        "id": 12,
        "texts": [
            "The more you practice, the better you become.",
            "The more you study, the smarter you become."
        ],
        "comment": "Comparative correlative pattern"
    },
    {
        "id": 13,
        "texts": [
            "There are many books on the shelf.",
            "There are many toys on the floor."
        ],
        "comment": "Existential 'there' pattern"
    },
    {
        "id": 14,
        "texts": [
            "What a beautiful day it is!",
            "What a wonderful time it was!"
        ],
        "comment": "Exclamatory sentence pattern"
    },
    {
        "id": 15,
        "texts": [
            "John, my best friend, lives nearby.",
            "Mary, my dear sister, works nearby."
        ],
        "comment": "Appositive phrase pattern"
    },
    {
        "id": 16,
        "texts": [
            "Having finished the work, she went home.",
            "Having completed the task, he went away."
        ],
        "comment": "Participial phrase pattern"
    },
    {
        "id": 17,
        "texts": [
            "It is important to exercise regularly.",
            "It is necessary to study consistently."
        ],
        "comment": "Extraposition pattern"
    },
    {
        "id": 18,
        "texts": [
            "The faster he runs, the more tired he gets.",
            "The harder she works, the more successful she becomes."
        ],
        "comment": "Complex comparative pattern"
    },
    {
        "id": 19,
        "texts": [
            "Either you come with us or stay here alone.",
            "Either we go together or stay here together."
        ],
        "comment": "Either-or coordination pattern"
    },
    {
        "id": 20,
        "texts": [
            "Despite being tired, she continued working hard.",
            "Despite being sick, he continued studying hard."
        ],
        "comment": "Concessive phrase pattern"
    }
]

def test_pattern_finder(base_url="http://127.0.0.1:5000"):
    """Pattern Finder Level 2のテストを実行"""
    results = []
    
    for test in test_cases:
        print(f"Testing case {test['id']}...")
        
        # APIリクエストの準備
        payload = {
            "texts": test["texts"],
            "level": 2  # Level 2: Token + POS
        }
        
        try:
            # APIを呼び出し
            response = requests.post(
                f"{base_url}/api/find-patterns",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # 結果の整形
                if data.get("success") and data.get("patterns"):
                    # 最も長いパターンを取得
                    top_patterns = data["patterns"][:3]  # 上位3つ
                    pattern_strs = []
                    for p in top_patterns:
                        pattern_strs.append(f"• {p['pattern']} (len:{p['length']}, count:{p['count']})")
                    output = "\n".join(pattern_strs)
                    status = "✅"
                else:
                    output = data.get("error", "No patterns found")
                    status = "❌"
            else:
                output = f"API Error: {response.status_code}"
                status = "❌"
                
        except Exception as e:
            output = f"Error: {str(e)}"
            status = "❌"
        
        # 結果を保存
        results.append({
            "#": test["id"],
            "Input": f"Text 1: \"{test['texts'][0]}\"\\nText 2: \"{test['texts'][1]}\"",
            "Output": output,
            "✔︎": status,
            "Comment": test["comment"]
        })
    
    return results

def save_results_to_markdown(results, filename="pattern_finder_level2_test_results.md"):
    """結果をマークダウンファイルに保存"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Pattern Finder Level 2 Test Results\n\n")
        f.write("**Test Date**: 2025-08-02  \n")
        f.write("**Level**: 2 (Token + POS)  \n")
        f.write("**Endpoint**: http://127.0.0.1:5000/  \n\n")
        
        # テーブルヘッダー
        f.write("| # | Input | Output | ✔︎ | Comment |\n")
        f.write("|---|-------|--------|---|---------|")
        
        # 各テスト結果
        for result in results:
            f.write(f"\n| {result['#']} | {result['Input']} | {result['Output']} | {result['✔︎']} | {result['Comment']} |")
        
        # サマリー
        success_count = sum(1 for r in results if r["✔︎"] == "✅")
        f.write(f"\n\n## Summary\n")
        f.write(f"- **Total Tests**: {len(results)}\n")
        f.write(f"- **Passed**: {success_count}\n")
        f.write(f"- **Failed**: {len(results) - success_count}\n")
        f.write(f"- **Success Rate**: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)\n")

if __name__ == "__main__":
    print("Pattern Finder Level 2 テストを開始します...")
    print("=" * 60)
    
    # テスト実行
    results = test_pattern_finder()
    
    # 結果を表示
    print("\nテスト結果:")
    print(tabulate(results, headers="keys", tablefmt="grid"))
    
    # マークダウンファイルに保存
    save_results_to_markdown(results)
    print(f"\n結果を pattern_finder_level2_test_results.md に保存しました。")
    
    # サマリー表示
    success_count = sum(1 for r in results if r["✔︎"] == "✅")
    print(f"\n成功: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")