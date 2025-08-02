#!/usr/bin/env python3
import requests
import json
from tabulate import tabulate

# テストケースの定義
test_cases = [
    {
        "id": 1,
        "texts": [
            "The happy children play in the garden.",
            "The excited students work in the classroom."
        ],
        "comment": "NP + VP + PP patterns"
    },
    {
        "id": 2,
        "texts": [
            "She quickly walked to the store.",
            "He slowly drove to the office."
        ],
        "comment": "ADVP + VP + PP patterns"
    },
    {
        "id": 3,
        "texts": [
            "The big red ball bounced high.",
            "The small blue car moved fast."
        ],
        "comment": "Complex NP with multiple modifiers"
    },
    {
        "id": 4,
        "texts": [
            "John gave Mary a beautiful gift.",
            "Sarah sent Tom a lovely card."
        ],
        "comment": "Double object VP pattern"
    },
    {
        "id": 5,
        "texts": [
            "After the meeting, we went home.",
            "Before the class, they ate lunch."
        ],
        "comment": "PP at sentence beginning"
    },
    {
        "id": 6,
        "texts": [
            "The book on the table is mine.",
            "The pen in the drawer is yours."
        ],
        "comment": "NP with embedded PP"
    },
    {
        "id": 7,
        "texts": [
            "Running quickly exhausted him completely.",
            "Swimming slowly relaxed her totally."
        ],
        "comment": "Gerund VP as subject"
    },
    {
        "id": 8,
        "texts": [
            "She seems very happy today.",
            "He looks quite tired now."
        ],
        "comment": "Linking verb + ADJP pattern"
    },
    {
        "id": 9,
        "texts": [
            "The teacher explained the lesson clearly to the students.",
            "The speaker presented the topic briefly to the audience."
        ],
        "comment": "Complex VP with ADVP and PP"
    },
    {
        "id": 10,
        "texts": [
            "In the morning, birds sing beautifully.",
            "At the night, owls hoot mysteriously."
        ],
        "comment": "PP + NP + VP + ADVP"
    },
    {
        "id": 11,
        "texts": [
            "The extremely talented musician played wonderfully.",
            "The incredibly skilled artist painted beautifully."
        ],
        "comment": "Intensified ADJP in NP"
    },
    {
        "id": 12,
        "texts": [
            "They found the solution surprisingly easy.",
            "We considered the problem remarkably simple."
        ],
        "comment": "Object complement with ADVP"
    },
    {
        "id": 13,
        "texts": [
            "Walking through the park, she saw many flowers.",
            "Jogging along the beach, he noticed several shells."
        ],
        "comment": "Participial phrase + main clause"
    },
    {
        "id": 14,
        "texts": [
            "To succeed in life, one must work hard.",
            "To excel at sports, you should practice daily."
        ],
        "comment": "Infinitive phrase pattern"
    },
    {
        "id": 15,
        "texts": [
            "The students studying hard will pass easily.",
            "The workers arriving early can leave sooner."
        ],
        "comment": "Reduced relative clause in NP"
    },
    {
        "id": 16,
        "texts": [
            "Both the cat and the dog sleep peacefully.",
            "Either the bus or the train arrives promptly."
        ],
        "comment": "Coordinated NP subjects"
    },
    {
        "id": 17,
        "texts": [
            "She not only sings beautifully but also dances gracefully.",
            "He not only writes clearly but also speaks eloquently."
        ],
        "comment": "Correlative conjunction with ADVP"
    },
    {
        "id": 18,
        "texts": [
            "The more carefully you study, the better you understand.",
            "The more diligently she works, the faster she progresses."
        ],
        "comment": "Comparative correlative with ADVP"
    },
    {
        "id": 19,
        "texts": [
            "Despite the heavy rain, they continued playing outside.",
            "Despite the strong wind, we kept walking forward."
        ],
        "comment": "Concessive PP + VP + ADVP"
    },
    {
        "id": 20,
        "texts": [
            "What she said yesterday surprised everyone greatly.",
            "What he did today shocked everybody completely."
        ],
        "comment": "Nominal clause as subject"
    }
]

def test_pattern_finder(base_url="http://127.0.0.1:5000"):
    """Pattern Finder Level 3のテストを実行"""
    results = []
    
    for test in test_cases:
        print(f"Testing case {test['id']}...")
        
        # APIリクエストの準備
        payload = {
            "texts": test["texts"],
            "level": 3  # Level 3: Token + Phrase Type
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
                    for i, p in enumerate(top_patterns, 1):
                        pattern_strs.append(f"{i}. \"{p['pattern']}\" ({p['length']} tokens, {p['count']} occurrences)")
                    output = f"Found {len(data['patterns'])} patterns:<br>" + "<br>".join(pattern_strs)
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
            "Input": f"Text 1: \"{test['texts'][0]}\"<br>Text 2: \"{test['texts'][1]}\"",
            "Output": output,
            "✔︎": status,
            "Comment": test["comment"]
        })
    
    return results

def save_results_to_markdown(results, filename="pattern_finder_level3_test_results.md"):
    """結果をマークダウンファイルに保存"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Pattern Finder Level 3 Test Results\n\n")
        f.write("**Test Date**: 2025-08-02  \n")
        f.write("**Level**: 3 (Token + Phrase Type)  \n")
        f.write("**Endpoint**: http://127.0.0.1:5000/  \n")
        f.write("**Note**: Level 3 excludes punctuation and identifies phrase types (NP, VP, PP, ADJP, ADVP, etc.)  \n\n")
        
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
        
        # フレーズタイプの説明
        f.write("\n## Phrase Type Legend\n")
        f.write("- **NP**: Noun Phrase\n")
        f.write("- **VP**: Verb Phrase\n")
        f.write("- **PP**: Prepositional Phrase\n")
        f.write("- **ADJP**: Adjective Phrase\n")
        f.write("- **ADVP**: Adverb Phrase\n")
        f.write("- **CONJP**: Conjunction Phrase\n")
        f.write("- **INFP**: Infinitive Phrase\n")
        f.write("- **O**: Other/No specific phrase type\n")

if __name__ == "__main__":
    print("Pattern Finder Level 3 テストを開始します...")
    print("=" * 60)
    
    # テスト実行
    results = test_pattern_finder()
    
    # 結果を表示
    print("\nテスト結果:")
    print(tabulate(results, headers="keys", tablefmt="grid"))
    
    # マークダウンファイルに保存
    save_results_to_markdown(results)
    print(f"\n結果を pattern_finder_level3_test_results.md に保存しました。")
    
    # サマリー表示
    success_count = sum(1 for r in results if r["✔︎"] == "✅")
    print(f"\n成功: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")