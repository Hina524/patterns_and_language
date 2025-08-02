# Pattern Finder Level 1 テスト結果（完全版）

## テスト実行日: 2025-08-02

### テスト3: 動物の行動パターン
- **入力テキスト:**
  - Text 1: "The cat sat on the mat."
  - Text 2: "The dog lay on the rug."
  - Text 3: "The bird flew on the branch."
- **結果:**
  - 見つかったパターン数: 4
  - 最も長いパターン: "on the"
  - 長さ: 2 tokens
  - 出現回数: 3

### テスト4: 動詞時制の違い
- **入力テキスト:**
  - Text 1: "I eat breakfast every morning."
  - Text 2: "I ate breakfast this morning."
- **結果:**
  - 見つかったパターン数: 3
  - 最も長いパターン: "I", "breakfast", "morning."（すべて1トークン）
  - 長さ: 1 token
  - 出現回数: 2

### テスト5: 現在形と現在進行形
- **入力テキスト:**
  - Text 1: "She walks to school."
  - Text 2: "She is walking to school."
- **結果:**
  - 見つかったパターン数: 4
  - 最も長いパターン: "to school."
  - 長さ: 2 tokens
  - 出現回数: 2

### テスト6: 完了形の比較
- **入力テキスト:**
  - Text 1: "They have finished the project."
  - Text 2: "They had finished the homework."
- **結果:**
  - 見つかったパターン数: 4
  - 最も長いパターン: "finished the"
  - 長さ: 2 tokens
  - 出現回数: 2

### テスト7: 未来形と条件法
- **入力テキスト:**
  - Text 1: "He will go to the party."
  - Text 2: "He would go to the meeting."
- **結果:**
  - 見つかったパターン数: 7
  - 最も長いパターン: "go to the"
  - 長さ: 3 tokens
  - 出現回数: 2

### テスト8: 前置詞（位置）
- **入力テキスト:**
  - Text 1: "The book is on the table."
  - Text 2: "The cat is under the chair."
- **結果:**
  - 見つかったパターン数: 3
  - 最も長いパターン: "The", "is", "the"（すべて1トークン）
  - 長さ: 1 token
  - 出現回数: 2

### テスト9: 前置詞（動き）
- **入力テキスト:**
  - Text 1: "She jumped over the fence."
  - Text 2: "He ran through the park."
  - Text 3: "They walked across the bridge."
- **結果:**
  - 見つかったパターン数: 1
  - 最も長いパターン: "the"
  - 長さ: 1 token
  - 出現回数: 3

### テスト10: 前置詞（方向）
- **入力テキスト:**
  - Text 1: "The gift is for my sister."
  - Text 2: "The letter is from my friend."
- **結果:**
  - 見つかったパターン数: 3
  - 最も長いパターン: "The", "is", "my"（すべて1トークン）
  - 長さ: 1 token
  - 出現回数: 2

### テスト11: 形容詞パターン
- **入力テキスト:**
  - Text 1: "The red car is fast."
  - Text 2: "The blue bike is slow."
- **結果:**
  - 見つかったパターン数: 2
  - 最も長いパターン: "The", "is"（すべて1トークン）
  - 長さ: 1 token
  - 出現回数: 2

### テスト12: 副詞パターン
- **入力テキスト:**
  - Text 1: "She sings very beautifully."
  - Text 2: "He speaks quite clearly."
- **結果:**
  - 見つかったパターン数: 0
  - 最も長いパターン: なし
  - 長さ: なし
  - 出現回数: なし

### テスト13: 強調副詞＋形容詞
- **入力テキスト:**
  - Text 1: "The extremely tall building stands there."
  - Text 2: "The incredibly fast train runs here."
  - Text 3: "The amazingly bright star shines above."
- **結果:**
  - 見つかったパターン数: 1
  - 最も長いパターン: "The"
  - 長さ: 1 token
  - 出現回数: 3

### テスト14: 等位接続詞（and）
- **入力テキスト:**
  - Text 1: "I want tea and she wants coffee."
  - Text 2: "He likes cats and she likes dogs."
- **結果:**
  - 見つかったパターン数: 3
  - 最も長いパターン: "and she"
  - 長さ: 2 tokens
  - 出現回数: 2

### テスト15: 従属接続詞（if）
- **入力テキスト:**
  - Text 1: "I will go if you come."
  - Text 2: "She will stay if he leaves."
- **結果:**
  - 見つかったパターン数: 2
  - 最も長いパターン: "will", "if"（すべて1トークン）
  - 長さ: 1 token
  - 出現回数: 2

### テスト16: 従属接続詞（because）
- **入力テキスト:**
  - Text 1: "I studied hard because I wanted to pass."
  - Text 2: "She worked late because she needed to finish."
  - Text 3: "They left early because they were tired."
- **結果:**
  - 見つかったパターン数: 1
  - 最も長いパターン: "because"
  - 長さ: 1 token
  - 出現回数: 3

### テスト17: 疑問文パターン
- **入力テキスト:**
  - Text 1: "What time does the meeting start?"
  - Text 2: "What time does the class begin?"
- **結果:**
  - 見つかったパターン数: 10
  - 最も長いパターン: "What time does the"
  - 長さ: 4 tokens
  - 出現回数: 2

### テスト18: 命令文パターン
- **入力テキスト:**
  - Text 1: "Don't forget to bring your book!"
  - Text 2: "Don't forget to submit your homework!"
- **結果:**
  - 見つかったパターン数: 7
  - 最も長いパターン: "Don't forget to"
  - 長さ: 3 tokens
  - 出現回数: 2

### テスト19: It構文
- **入力テキスト:**
  - Text 1: "It's important to stay healthy."
  - Text 2: "It's necessary to work hard."
- **結果:**
  - 見つかったパターン数: 2
  - 最も長いパターン: "It's", "to"（すべて1トークン）
  - 長さ: 1 token
  - 出現回数: 2

### テスト20: There構文
- **入力テキスト:**
  - Text 1: "There are many books on the shelf."
  - Text 2: "There are several students in the classroom."
- **結果:**
  - 見つかったパターン数: 4
  - 最も長いパターン: "There are"
  - 長さ: 2 tokens
  - 出現回数: 2

## まとめ
Pattern Finder Level 1の全20テストを完了しました。最も長いパターンを検出したのはテスト17の疑問文パターンで、"What time does the"という4トークンのパターンが見つかりました。多くのテストで共通の構造や語彙が正しく検出されており、Pattern Finderが適切に機能していることが確認できました。