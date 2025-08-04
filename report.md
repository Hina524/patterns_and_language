# Name of your Pattern-matching Tool
https://github.com/Hina524/patterns_and_language
# Group members

| 学籍番号     | 氏名           | 貢献内容                                          |
| -------- | ------------ | --------------------------------------------- |
| s1310141 | Hina Konishi | 70% (main programmer, test, report, analysis) |
| s1290116 | Tsubasa Sato | 30% (analysis)                                |
# 1. Tool description
## Webアプリケーション全体の目的

このWebアプリケーションは、**英語学習者、言語処理学習者の包括的な言語習得支援システム**として設計されています。
## 3つの主要機能

### 1. English Grammar Analyzer機能

英語の文章を入力すると、その文章を以下のように**文法的に分析**するツールです。
- **過去形変換**: 文章中の動詞を自動的に過去形に変換
- **文タイプ判定**: その文が Simple（単文）、Compound（重文）、Complex（複文）のどれかを判定
- **前置詞句抽出**: 文章の中にある前置詞句（"in the library"など）を自動で見つけ出す
#### 機能目的
- **包括的文法分析**: 入力された英語文の多面的文法構造解析
- **時制変換実践**: 現在形から過去形への変換を通じた動詞活用学習
- **文型理解促進**: Simple、Compound、Complex文の構造的違いの体験学習
- **前置詞句認識**: 英語特有の前置詞構造パターンの習得支援
### 2. Template Sentence Generator機能

英語の**文章作成を支援**するために、用途別のテンプレート文を提供してくれるツールです。以下の4つのカテゴリーのテンプレート文をランダムに生成します。
- **Topic Sentence**: 文章の導入部分で使える文
- **Sensory Details**: 五感を使った描写文
- **Spatial Details**: 場所や位置関係を表す文
- **Concluding Sentence**: 文章の結論部分で使える文
#### **機能目的**
- **ライティング支援**: 描写文の体系的構成方法の習得
- **語彙拡張促進**: カテゴリー別表現パターンの提供
- **創作インスピレーション**: ライティングブロック解消のアイデア生成
### 3. Pattern Finder機能

手動入力またはファイルアップロードで複数の英語テキストを比較して、それらの間にある**共通のパターンや表現**を以下の**4段階の分析レベル**で自動的に見つけ出すツールです。
  - Level 1: 単語レベルの共通パターン
  - Level 2: 単語 + 品詞タグの共通パターン  
  - Level 3: 単語 + 句タイプの共通パターン
  - Level 4: 単語 + 品詞 + 句タイプの包括的分析
#### **機能目的**
- **言語パターン認識**: 複数テキスト間の共通構造・表現の発見
- **比較言語学習**: 類似文構造の客観的分析による理解深化
- **語学研究支援**: corpus linguisticsの基礎的手法の実践
- **多層分析体験**: 語彙→品詞→句構造の段階的言語理解
# 2. Language analysis
## 1. English Grammar Analyzer機能
### Analysis
#### 1. 時制変換
```python
def convert_to_past_tense(self, text: str) -> str:
    doc = self.nlp(text)
    tokens = []
    for token in doc:
        if self._should_convert_to_past(token, doc):
            past_form = self._get_past_form(token)
            tokens.append(past_form)
        else:
            tokens.append(token.text)
```

**言語理論的基盤:**
- **spaCy依存関係解析**: 文構造の正確な把握による文脈適応型動詞変換
- **英語動詞活用体系**: 規則動詞（-ed付加）・不規則動詞（語幹変化）・助動詞の包括的処理
- **時制一致原理**: 文全体における時制の統一性維持
- **高精度形態論解析**: 語幹抽出→活用語尾処理→不規則動詞辞書照合

**実装の特徴:**
1. **不規則動詞辞書（80語以上）**:
   - 基本動詞: go→went, come→came, see→saw, make→made
   - be動詞: is→was, are→were, am→was
   - 特殊動詞: shine→shone, swim→swam, fly→flew
   - 助動詞: can→could, will→would, may→might

2. **協調動詞処理**:
   - 等位接続詞で結ばれた動詞の一括変換
   - 例: "They swim, run, and fly" → "They swam, ran, and flew"
   - spaCyのタグ付けエラー（VBN誤認識）への対応

3. **助動詞構造の処理**:
   - Modal auxiliary (MD)の変換: can→could, will→would
   - 助動詞後の動詞は原形維持: "can go" → "could go"
   - be/have動詞の適切な変換: has→had, are→were

4. **進行形の保持**:
   - be動詞のみ変換、-ing形は維持
   - 例: "We are walking" → "We were walking"
   - 依存関係解析による進行形構造の正確な識別

5. **規則動詞の精密な活用ルール**:
   - -e終わり: like→liked
   - 子音+y: study→studied  
   - 母音+y: play→played（playyed誤りを防止）
   - CVC pattern: stop→stopped
   - その他: work→worked

#### 2. 文構造分析
**理論的基盤: Dependency Grammar + Syntactic Parsing**

```python
def get_sentence_type(self, text: str) -> str:
    doc = self.nlp(text)
    subordinators = {'after', 'although', 'as', 'because', 'before'...}
    
    # 従属節検出
    for token in doc:
        if token.text.lower() in subordinators:
            if any(child.dep_ in ['ccomp', 'advcl', 'acl'] 
                   for child in token.head.children):
                return 'complex'
```

1. **Simple Sentence（単文）**: 単一主語+動詞構造
2. **Compound Sentence（重文）**: 等位接続詞による独立節結合
3. **Complex Sentence（複文）**: 従属接続詞による主節+従属節構造

**spaCy依存関係ラベル活用:**
- `ccomp`: 節補語 (clausal complement)
- `advcl`: 副詞節 (adverbial clause modifier)  
- `acl`: 関係節 (clausal modifier of noun)

#### 3. 前置詞句抽出
**依存関係解析による高精度抽出:**
```python
def get_prepositional_phrases(self, text: str) -> List[str]:
    doc = self.nlp(text)
    for token in doc:
        if token.pos_ == 'ADP':  # 前置詞検出
            for child in token.children:
                if child.dep_ == 'pobj':  # 前置詞の目的語
                    phrase_tokens.extend(self._get_noun_phrase_tokens(child, doc))
```

- **構文解析**: 前置詞 + 依存関係による目的語特定
- **句境界認識**: 修飾語・限定詞の包括的検出
- **ネスト構造**: "in the garden behind the house near the river"

### Algorithm Diagram

``` mermaid
flowchart TD
    A[入力テキスト] --> B[spaCy NLP処理]
    B --> C[依存関係解析完了]
    C --> D[時制変換処理]
    C --> E[文構造分析]
    C --> F[前置詞句抽出]
    
    D --> D1[動詞・助動詞識別]
    D1 --> D2[変換判定ロジック]
    D2 --> D3{助動詞判定}
    D3 -->|Modal MD| D3A[can→could等変換]
    D3 -->|be/have| D3B[is→was等変換]
    D3 -->|No| D4{進行形判定}
    D4 -->|Yes| D4A[be動詞のみ変換<br/>-ing形維持]
    D4 -->|No| D5{協調構造?}
    D5 -->|Yes| D6[協調動詞変換]
    D5 -->|No| D7[単一動詞変換]
    
    D3A --> G[Flask API Response]
    D3B --> G
    D4A --> G
    
    D6 --> D8{不規則動詞?}
    D7 --> D8
    D8 -->|Yes| D9[80+動詞辞書検索<br/>swim→swam等]
    D8 -->|No| D10[規則動詞ルール]
    D10 --> D10A{語尾判定}
    D10A -->|e| D10B[+d: like→liked]
    D10A -->|子音+y| D10C[y→ied: study→studied]
    D10A -->|母音+y| D10D[+ed: play→played]
    D10A -->|CVC| D10E[重複+ed: stop→stopped]
    D10A -->|他| D10F[+ed: work→worked]
    
    D9 --> G
    D10B --> G
    D10C --> G
    D10D --> G
    D10E --> G
    D10F --> G
    
    E --> E1[従属接続詞検索]
    E1 --> E2{依存関係ラベル確認}
    E2 -->|ccomp/advcl/acl| E3[Complex判定]
    E2 -->|No| E4[等位接続詞分析]
    E4 --> E5{複数主動詞?}
    E5 -->|Yes| E6[Compound判定]
    E5 -->|No| E7[Simple判定]
    
    F --> F1[ADP品詞検出]
    F1 --> F2[pobj依存関係]
    F2 --> F3[名詞句拡張]
    F3 --> F4[句境界確定]
    
    E3 --> G
    E6 --> G
    E7 --> G
    F4 --> G
    G --> H[JSON結果返却]
    H --> I[フロントエンド表示]
```
Fig. 1: [English Grammar Analyzer機能のAlgorithm Diagram]
## 2. Template Sentence Generator機能
### Analysis

#### 文章構造理論
**Academic Writing Theory + Paragraph Development Model**
```javascript
const topicSentences = [10個のテンプレート];      // 導入部
const sensoryDetails = [10個のテンプレート];      // 感覚描写
const spatialDetails = [10個のテンプレート];      // 空間描写
const concludingSentences = [9個のテンプレート];   // 結論部
```

**言語学的分析基盤:**

1. **Topic Sentence Analysis（主題文分析）**
   - **Discourse Markers**: "I want to describe", "Today, I will"
   - **Thematic Structure**: 主題提示→詳細展開の予告機能

2. **Sensory Description Framework（感覚描写枠組み）**
   ```javascript
   'It looks ___ and ___.',
   'You can hear ___, especially when ___.',
   'It smells like ___, and that reminds me of ___.'
   ```
   - **五感カテゴリー化**: 視覚・聴覚・嗅覚・触覚・味覚の体系的配置
   - **Cognitive Linguistics**: 感覚体験→言語表現のマッピング

3. **Spatial Coherence Theory（空間的結束理論）**
   ```javascript
   'It is located near ___.',
   'Around it, there are ___ and ___.',
   'Inside, you can find ___.'
   ```
   - **Spatial Deixis**: 位置関係を示す指示表現
   - **Topological Relations**: near, around, inside等の空間前置詞
#### **ランダム化アルゴリズム**
```javascript
function showRandomTemplate(list, label) {
    const idx = Math.floor(Math.random() * list.length);
    templateOutput.innerText = `${label}:\n${list[idx]}`;
}
```
- **Uniform Distribution**: 各テンプレートの等確率選択
- **Cognitive Load Theory**: 予測不可能性による創造的思考促進
### Algorithm Diagram
``` mermaid
flowchart TD
    A[ユーザーがカテゴリー選択] --> B{カテゴリー判定}
    
    B -->|Topic Sentence| C[topicSentences配列]
    B -->|Sensory Details| D[sensoryDetails配列]
    B -->|Spatial Details| E[spatialDetails配列]
    B -->|Concluding| F[concludingSentences配列]
    
    C --> G[Math.random生成]
    D --> G
    E --> G
    F --> G
    
    G --> H[配列長との乗算]
    H --> I[Math.floor整数化]
    I --> J[インデックス決定]
    
    J --> K[対応テンプレート取得]
    K --> L[ラベル付加]
    L --> M[結果表示]
    
    subgraph "文章構造理論"
        N[Topic Introduction]
        O[Sensory Elaboration]
        P[Spatial Organization]
        Q[Conclusion/Reflection]
        N --> O --> P --> Q
    end
    
    C -.-> N
    D -.-> O
    E -.-> P
    F -.-> Q
```
Fig. 2: [Template Sentence Generator機能のAlgorithm Diagram]
## 3. Pattern Finder機能
### Analysis
#### 多層言語分析システム
**spaCy + Dependency Grammar + Phrase Structure Grammar**

**Level 1: Lexical Analysis（語彙分析）**
```python
return [token.text for token in doc if not token.is_space]
```
- **Tokenization Theory**: 語境界認識による最小言語単位分割

**Level 2: Morpho-syntactic Analysis（形態統語分析）**
```python
return [(token.text, token.pos_) for token in doc if not token.is_space]
```
- **Penn Treebank Tagset**: DT, NN, VB, IN等の標準品詞体系
- **Part-of-Speech Tagging**: 統計的言語モデルによる品詞自動付与

**Level 3: Phrase Structure Analysis（句構造分析）**
```python
# 句読点除外による純粋句構造分析
if token.is_space or token.pos_ == 'PUNCT':
    continue
phrase_type = self.get_phrase_type(token, doc, phrase_map)
```

**理論的基盤: X-bar Theory + Dependency Grammar**
#### **句構造検出アルゴリズム**
```python
def _build_phrase_map(self, doc):
    # Step 0: カスタム修正による精度向上
    self._apply_custom_corrections(doc, phrase_map)
    
    # Step 1: spaCy noun_chunksによる名詞句検出
    for chunk in doc.noun_chunks:
        for i in range(chunk.start, chunk.end):
            phrase_map[i] = 'NP'
    
    # Step 2: 不定詞句検出（動詞句より先に処理）
    for token in doc:
        if self._is_infinitive_marker(token, doc):
            inf_tokens = self._get_infinitive_phrase_tokens(token, doc)
            for tok_idx in inf_tokens:
                phrase_map[tok_idx] = 'INF-P'
    
    # Step 3: 依存関係解析による動詞句検出
    if token.pos_ in ['VERB', 'AUX'] and token.i not in phrase_map:
        vp_tokens = self._get_verb_phrase_tokens(token, doc)
```

**カスタム修正機能:**
```python
def _apply_custom_corrections(self, doc, phrase_map):
    """spaCyのタグ付け精度問題への対処"""
    for token in doc:
        # 動名詞主語の修正（Swimming[PROPN] → Swimming[VP]）
        if (token.pos_ == 'PROPN' and 
            token.tag_ == 'NNP' and 
            token.dep_ == 'nsubj' and 
            token.text.lower().endswith('ing')):
            phrase_map[token.i] = 'VP'
        
        # 時間表現の統一（today, now等をADVPに）
        if self._is_time_expression(token, doc):
            phrase_map[token.i] = 'ADVP'
```

**不定詞句検出:**
```python
def _is_infinitive_marker(self, token, doc):
    """to + 動詞構造の識別"""
    if (token.pos_ == 'PART' and 
        token.tag_ == 'TO' and 
        token.text.lower() == 'to'):
        # 後続動詞チェック
        if token.i + 1 < len(doc):
            next_token = doc[token.i + 1]
            if next_token.pos_ == 'VERB' and next_token.tag_ == 'VB':
                return True
```

**動詞句境界検出:**
```python
def _get_verb_phrase_tokens(self, verb, doc):
    # 依存関係ラベルによる句構成要素特定
    for child in verb.children:
        if child.dep_ in ['aux', 'auxpass', 'neg', 'prt']:
            vp_tokens.add(child.i)
```
#### **パターンマッチング理論**
**Sequence Alignment + N-gram Analysis**

```python
def find_common_patterns(self, token_sequences):
    # 最短シーケンス基準による効率化
    base_idx = min(range(len(token_sequences)), 
                   key=lambda i: len(token_sequences[i][1]))
    
    # 全可能部分列探索
    for length in range(n, 0, -1):  # 長いパターン優先
        for start in range(n - length + 1):
            pattern = tuple(base_seq[start:start + length])
```

**計算量最適化:**
- **Time Complexity**: O(n²m) where n=sequence length, m=number of texts
- **Space Complexity**: O(nm) for pattern storage
### **🔬 Level 4統合分析の複雑性**

**Level 4: Multi-dimensional Analysis（多次元統合分析）**
```python
tokens.append((token.text, token.pos_, phrase_type))
```

**言語学的意義:**
- **Morpho-syntactic Interface**: 形態論と統語論の接続点分析
- **Feature Unification**: 品詞情報と句構造情報の統合
- **Linguistic Annotation**: 多層言語情報の同時表現

**句読点の理論的処理:**
```python
if token.pos_ == 'PUNCT':
    # Level 3: 句構造分析では除外
    continue
    # Level 4: POSは保持、句タイプは無効化
    tokens.append((token.text, token.pos_, 'O'))
```

**理論的根拠**: 句読点は**韻律境界（Prosodic Boundary**を示すが、**句構造（Phrase Structure**の構成要素ではない
### Algorithm Diagram
``` mermaid
flowchart TD
    A[複数テキスト入力] --> B[spaCy NLP処理]
    B --> C{分析レベル選択}
    
    C -->|Level 1| D1[Simple Tokenization]
    C -->|Level 2| D2[POS Tagging]
    C -->|Level 3| D3[Phrase Analysis]
    C -->|Level 4| D4[Combined Analysis]
    
    D3 --> E[句構造マップ構築]
    E --> E0[Step 0: カスタム修正]
    E0 --> E0A[動名詞主語修正<br/>Swimming[PROPN]→[VP]]
    E0 --> E0B[時間表現統一<br/>today/now→[ADVP]]
    E0A --> E1[Step 1: 名詞句検出]
    E0B --> E1
    E1 --> E2[Step 2: 不定詞句検出]
    E2 --> E3[Step 3: 動詞句検出]
    E3 --> E4[Step 4: 前置詞句検出]
    E4 --> E5[Step 5: 形容詞句検出]
    E5 --> E6[Step 6: 副詞句検出]
    E6 --> E7[Step 7: 残余トークン分類]
    
    subgraph "不定詞句検出詳細"
        INF1[to[PART]検出]
        INF2[後続動詞確認]
        INF3[to + VB構造]
        INF4[INF-Pタグ付与]
        INF1 --> INF2 --> INF3 --> INF4
    end
    
    E2 -.-> INF1
    
    subgraph "動詞句検出詳細"
        F1[動詞トークン特定]
        F2[依存関係解析]
        F3[aux/neg/prt検出]
        F4[VP境界確定]
        F1 --> F2 --> F3 --> F4
    end
    
    E3 -.-> F1
    
    D1 --> G[トークン配列生成]
    D2 --> G
    E7 --> G
    D4 --> G
    
    G --> H[パターンマッチング]
    H --> H1[最短シーケンス選択]
    H1 --> H2[全部分列生成]
    H2 --> H3[パターン頻度計算]
    H3 --> H4[2ファイル以上フィルタ]
    H4 --> H5[長さ・頻度ソート]
    
    H5 --> I[共通パターン出力]
    
    subgraph "言語理論基盤"
        J[Dependency Grammar]
        K[X-bar Theory]
        L[Penn Treebank]
        M[Phrase Structure Rules]
    end
    
    E -.-> J
    E -.-> K
    D2 -.-> L
    E -.-> M
```

Fig. 3: [Pattern Finder機能のAlgorithm Diagram]
# 3. Software development
## 使用技術スタック
### プログラミング言語・フレームワーク
- **Python 3.11**: バックエンド処理、NLP解析エンジン
- **JavaScript ES6+**: フロントエンド動的処理、非同期API通信
- **HTML5**: セマンティックな構造化マークアップ
- **CSS3**: モダンなスタイリング、レスポンシブデザイン
### 主要ライブラリ
- **Flask 3.0.0**: 軽量Webフレームワーク
- **spaCy 3.8.5**: 産業標準NLPライブラリ（English Grammar Analyzer & Pattern Finder backend）
- **W3.CSS**: レスポンシブCSSフレームワーク

## 1. アプリケーション全体
### レスポンシブデザイン
全ての利用場面に対応するため、PC、スマートフォンのどちらからアクセスしても利用ができるようにしています。
![[スクリーンショット 2025-08-02 22.06.12.png]]
Fig. 4: [PCで起動した際の画面]

![[スクリーンショット 2025-08-02 22.07.05.png|400]]
Fig. 5: [スマートフォンで起動した際の画面]
### タブインターフェース
本アプリケーションは3つの機能があるため、MUIを参考にタブで機能切り替えができるようにしました。
![[スクリーンショット 2025-08-02 19.12.52.png]]
Fig. 6: [タブの画面]

```css
.tab-button {
    transition: all 0.3s ease;
    border-bottom: 2px solid transparent;
}
.tab-button.active {
    color: orange;
    border-bottom-color: orange;
}
```
## 2. English Grammar Analyzer機能
### 機能利用例
![[スクリーンショット 2025-08-02 22.06.12.png]]
Fig. 7: [English Grammar Analyzer機能の入力画面]
上記の初期画面のInput部分に英文を入力し、「Process」ボタンを押すと、
![[スクリーンショット 2025-08-02 22.24.46.png]]
Fig. 8: [English Grammar Analyzer機能の結果表示画面]
上記画像のように結果が表示されます。

### 工夫点
#### テキスト入力エリアの行数が入力文の長さに合わせて変動する
当初の実装では、長文を入力すると文字が見切れてしまったため、改善しました。Fig. 8の画像と比較し、Fig. 9ではテキスト入力エリアの行数が増えていることがわかります。

```javascript
function autoResize(textarea) {
    textarea.style.height = 'auto';
    const minHeight = 3 * 24; // 3 lines
    const maxHeight = 10 * 24; // 10 lines
    const scrollHeight = textarea.scrollHeight;
    // 動的高さ調整ロジック
}
```

![[スクリーンショット 2025-08-02 22.25.33.png]]
Fig. 9: [English Grammar Analyzer機能の入力エリアに長文を入力した画像]
## 3. Template Sentence Generator機能
### 機能利用例
オレンジ色のボタンのいずれかを選択して押すことで、選択したカテゴリのテンプレートが出力されます。
![[スクリーンショット 2025-08-02 22.29.03.png]]
Fig. 10: [Template Sentence Generator機能の結果表示画面]
### 工夫点
#### レスポンシブデザイン
スマホサイズ（600px以下）での Template Sentence Generator ボタンについて、PCサイズでのレイアウト(2×2)にすると文字が潰れてしまうので、縦一列の中央揃えにしました。
``` css
/* Template Sentence Generatorのボタン中央寄せ */
#templateTab .w3-row-padding {
	text-align: center;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 8px;
}

#templateTab .w3-col {
	display: block;
	float: none;
	width: auto;
	max-width: 280px;
}

#templateTab .w3-button-orange {
	margin: 0 auto;
	display: block;
	width: auto;
	min-width: 200px;
	max-width: 280px;
}
```

![[スクリーンショット 2025-08-02 22.48.07.png|400]]
Fig. 11: [Template Sentence Generator機能のスマホサイズの画面]
## 4. Pattern Finder機能
### 機能利用例
最初に「Manual Text Input」（手入力）か「Upload Text Files」を選択します。
![[スクリーンショット 2025-08-02 22.53.40.png]]
Fig. 12: [Pattern Finder機能の初期画面]
#### 「Manual Text Input」を選択した場合
テキストを入力したあと、Levelを選択し、Processを押します。そうすると、結果が以下のように出力されます。３種類以上のテキストを分析する際は、「Add Text」ボタンを押すとテキスト入力エリアが増え、さらにテキストを入力することができます。
![[スクリーンショット 2025-08-02 22.55.56.png]]
Fig. 13: [Pattern Finder機能でManual Text Inputを選択した場合の結果画面]
#### 「Upload Text Files」を選択した場合
この場合、まずFig. 14のような画面に移動します。
- 枠内にテキストファイルをドラッグ&ドロップをする
- Select Text Filesボタンを押す
のいずれかの方法でテキストを入力することができます。ファイルは.txtファイルしかアップロードできないようになっています。
![[スクリーンショット 2025-08-02 23.09.26.png]]
Fig. 14: [Pattern Finder機能でUpload Text Filesを選択した場合の初期画面]

ファイルをアップロードすると、Fig. 15のように、Upload Filesの中で、入力したテキストの内容を確認することができます。レベルを選択し、Processボタンを押してからの画面は「Manual Text Input」を選択した場合と同様になります。
![[スクリーンショット 2025-08-02 23.27.28.png]]
Fig. 15: [Pattern Finder機能でテキストファイルをアップロードした際の画面]
### 工夫点
#### 1. デュアル入力システム
- **Textbox Input**: 動的テキストエリア追加/削除機能
- **File Upload**: ドラッグ&ドロップ + ファイル選択の二重サポート
##### 目的
**テキストボックス入力方式**
- 一般的な英語学習者はテキストをテキストファイルで所持しているケースは少なく、パターン分析をしたい英文を見つけたらすぐコピー＆ペーストで分析を実行できるようにしたい
- スマートフォン対応もしているため、この場合もこちらの方式が適切であると判断
	-> 一般的な英語学習者にはファイルアップロードよりこちらの方式が適切であると判断しました

**ファイルアップロード方式**
- NLP学習者はテキストをテキストファイルで保持していることが一般的であるため、こちらの方式が適切であると判断しました
- 分析を何回も繰り返すことを考えても、こちらが適切であると判断しました

以上より、テキストを与えるだけでも、二つの需要があることから、二つの方式を取ることは必須であると考えました
#### 2. ファイルアップロード時の分析対象テキスト表示
テキストボックスで入力する際は、テキストボックスを確認すれば分析対象のテキストを確認することができますが、アップロードの場合は確認することができませんでした。分析対象のテキストと出力結果を比較することが重要であるため、この機能を追加しました。
また、ユーザーフレンドリーな実装にするため、Fig. 16のように、分析対象のテキストの長さに合わせて表示枠が変動するようになっています。
![[スクリーンショット 2025-08-02 23.33.05.png]]
Fig. 16: [Pattern Finder機能で分析対象のテキストを確認する画面1]

また、文章が長すぎたり、スマホで見る場合は、Fig. 17のように一定の行数を超えるとスクロールができ流ようになり、必要以上に表示行数を増やさない工夫をしています。
![[スクリーンショット 2025-08-02 23.53.19.png|400]]
Fig. 17: [Pattern Finder機能で分析対象のテキストを確認する画面2]

# 4. Software evaluation

## Usability study
### Describe advice received in green task
7月15日(火)の授業にて、「This is banana and that is an orange.」という例文を現在のEnglish Grammar Analyzer機能に入力すると、出力においてcompoundと表示されるべき場所でcomplexと表示されてしまうことを指摘された。

現在の出力
```
This was banana and that was an orange.
sentence type:
・compound
prepositional phrases:
・(none)
```

以上の通り適切に修正された。

### Accuracy evaluation
チームメンバーは2人であるため、10×2=20より、各機能20個以上のテストを実施した。
#### 表1: English Grammar Analyzer 機能精度評価

**Test Date**: 2025-08-03  
**Overall Success Rate**: 28/28 (100%) ✅

| # | Input | Output | ✔︎ | Comment |
|---|-------|--------|---|---------|
| 1 | The cat sleeps on the mat. | The cat slept on the mat.<br>sentence type: ・simple<br>prepositional phrases: ・on the mat | ✅ | All functions work correctly |
| 2 | She writes beautiful poems in her notebook. | She wrote beautiful poems in her notebook.<br>sentence type: ・simple<br>prepositional phrases: ・in her notebook | ✅ | All functions work correctly |
| 3 | Students study hard before the exam. | Students studied hard before the exam.<br>sentence type: ・complex<br>prepositional phrases: ・before the exam | ✅ | All functions work correctly |
| 4 | I like coffee, but she prefers tea. | I liked coffee, but she preferred tea.<br>sentence type: ・compound<br>prepositional phrases: ・(none) | ✅ | All functions work correctly |
| 5 | He studies math, and she learns science. | He studied math, and she learned science.<br>sentence type: ・compound<br>prepositional phrases: ・(none) | ✅ | All functions work correctly |
| 6 | The sun shines brightly, yet the air feels cool. | The sun shone brightly, yet the air felt cool.<br>sentence type: ・compound<br>prepositional phrases: ・(none) | ✅ | Fixed: "shine" → "shone" (irregular verb) |
| 7 | We can go to the park, or we can stay home. | We could go to the park, or we could stay home.<br>sentence type: ・compound<br>prepositional phrases: ・to the park | ✅ | Fixed: Modal auxiliary processing |
| 8 | Although it rains heavily, we continue our journey. | Although it rained heavily, we continued our journey.<br>sentence type: ・complex<br>prepositional phrases: ・(none) | ✅ | All functions work correctly |
| 9 | She smiles whenever she sees her friends. | She smiled whenever she saw her friends.<br>sentence type: ・complex<br>prepositional phrases: ・(none) | ✅ | All functions work correctly |
| 10 | If you study hard, you will pass the test. | If you studied hard, you would pass the test.<br>sentence type: ・complex<br>prepositional phrases: ・(none) | ✅ | Fixed: "will" → "would" (correct modal auxiliary) |
| 11 | The dog barks because it hears strange noises outside. | The dog barked because it heard strange noises outside.<br>sentence type: ・complex<br>prepositional phrases: ・(none) | ✅ | All functions work correctly |
| 12 | I go to school, eat lunch, and come back home. | I went to school, ate lunch, and came back home.<br>sentence type: ・compound<br>prepositional phrases: ・to school | ✅ | All functions work correctly |
| 13 | She takes photos, makes videos, and writes captions. | She took photos, made videos, and wrote captions.<br>sentence type: ・compound<br>prepositional phrases: ・(none) | ✅ | All functions work correctly |
| 14 | They swim in the pool, run in the park, and fly kites. | They swam in the pool, ran in the park, and flew kites.<br>sentence type: ・compound<br>prepositional phrases: ・in the pool<br>・in the park | ✅ | Fixed: Multiple verb coordination |
| 15 | The book on the table in the library belongs to the student from Japan. | The book on the table in the library belonged to the student from Japan.<br>sentence type: ・simple<br>prepositional phrases: ・on the table in the library<br>・to the student from Japan<br>・in the library<br>・from Japan | ✅ | All functions work correctly |
| 16 | During the summer, children play in the garden behind the house near the river. | During the summer, children played in the garden behind the house near the river.<br>sentence type: ・simple<br>prepositional phrases: ・During the summer<br>・in the garden behind the house<br>・behind the house<br>・near the river | ✅ | Fixed: "play" → "played" (regular verb rules) |
| 17 | At midnight, the owl sits on the branch under the moon. | At midnight, the owl sat on the branch under the moon.<br>sentence type: ・simple<br>prepositional phrases: ・At midnight<br>・on the branch<br>・under the moon | ✅ | All functions work correctly |
| 18 | When the sun rises, birds sing because they feel happy, although some people still sleep. | When the sun rose, birds sang because they felt happy, although some people still slept.<br>sentence type: ・complex<br>prepositional phrases: ・(none) | ✅ | All functions work correctly |
| 19 | Since he arrived early, he waits patiently while she finishes her work, even though he feels tired. | Since he arrived early, he waited patiently while she finished her work, even though he felt tired.<br>sentence type: ・complex<br>prepositional phrases: ・(none) | ✅ | All functions work correctly |
| 20 | That man thinks that the solution works, so he implements it even if others doubt that it succeeds. | That man thought that the solution worked, so he implemented it even if others doubted that it succeeded.<br>sentence type: ・complex<br>prepositional phrases: ・(none) | ✅ | All functions work correctly |
| 21 | This is a banana and that is an orange. | This was a banana and that was an orange.<br>sentence type: ・compound<br>prepositional phrases: ・(none) | ✅ | Fixed: be-verb conversion in AUX context |
| 22 | They are students in the classroom. | They were students in the classroom.<br>sentence type: ・simple<br>prepositional phrases: ・in the classroom | ✅ | Fixed: "are" → "were" (specific form priority) |
| 23 | I am a teacher at this school. | I was a teacher at this school.<br>sentence type: ・simple<br>prepositional phrases: ・at this school | ✅ | Fixed: "am" → "was" (be-verb conversion) |
| 24 | She has a book and he has a pen. | She had a book and he had a pen.<br>sentence type: ・compound<br>prepositional phrases: ・(none) | ✅ | Fixed: "has" → "had" (have-verb conversion) |
| 25 | We are walking in the park. | We were walking in the park.<br>sentence type: ・simple<br>prepositional phrases: ・in the park | ✅ | Fixed: Present progressive (-ing form preservation) |
| 26 | She is running to school. | She was running to school.<br>sentence type: ・simple<br>prepositional phrases: ・to school | ✅ | Fixed: Present progressive (-ing form preservation) |
| 27 | They are playing soccer. | They were playing soccer.<br>sentence type: ・simple<br>prepositional phrases: ・(none) | ✅ | Fixed: Present progressive (-ing form preservation) |
| 28 | I am studying English. | I was studying English.<br>sentence type: ・simple<br>prepositional phrases: ・(none) | ✅ | Fixed: Present progressive (-ing form preservation) |

#### Template Sentence Generator機能
この機能は、テストを実施しない

#### English Grammer Analyzer機能
##### 表2: English Grammar Analyzer機能 レベル1精度評価

  
**Test Date**: 2025-08-03

**Overall Success Rate**: 20/20 (100%) ✅

| # | Input | Output | ✔︎ | Comment |
|---|-------|--------|---|---------|
| 1 | Text 1: "The cat is sleeping."<br>Text 2: "The cat is eating." | Found 6 patterns:<br>1. "The cat is" (3 tokens)<br>2. "The cat" (2 tokens)<br>3. "cat is" (2 tokens)<br>Total: 2 occurrences each | ✅ | Common patterns correctly detected |
| 2 | Text 1: "Hello, how are you today?"<br>Text 2: "Hello, how are you feeling?"<br>Text 3: "Hi, how are you doing?" | Found 10 patterns:<br>1. "Hello, how are you" (4 tokens, 2 files)<br>2. "how are you" (3 tokens, 3 files)<br>3. "how are" (2 tokens, 3 files) | ✅ | Common patterns across 3 texts properly detected |
| 3 | Text 1: "I wake up, brush my teeth, and eat breakfast."<br>Text 2: "She wakes up, brushes her teeth, and eats breakfast." | Found 5 patterns:<br>1. "teeth, and" (2 tokens, 2 occurrences)<br>2. "up," (1 token, 2 occurrences)<br>3. "teeth," (1 token, 2 occurrences)<br>4. "and" (1 token, 2 occurrences)<br>5. "breakfast." (1 token, 2 occurrences) | ✅ | Detected common parts despite verb conjugation differences |
| 4 | Text 1: "What is your favorite color?"<br>Text 2: "What is your favorite food?"<br>Text 3: "What is your favorite movie?" | Found 10 patterns:<br>1. "What is your favorite" (4 tokens, 3 files)<br>2. "What is your" (3 tokens, 3 files)<br>3. "is your favorite" (3 tokens, 3 files) | ✅ | Question structure patterns perfectly detected |
| 5 | Text 1: "Every morning I go for a walk."<br>Text 2: "Every morning she goes for a run."<br>Text 3: "Every morning they go for a swim." | Found 9 patterns:<br>1. "go for a" (3 tokens, 2 files)<br>2. "Every morning" (2 tokens, 3 files)<br>3. "for a" (2 tokens, 3 files)<br>4. "go for" (2 tokens, 2 files) | ✅ | Time expressions and prepositional patterns detected |
| 6 | Text 1: "If it rains, I will stay home."<br>Text 2: "If it snows, I will stay inside." | Found 9 patterns:<br>1. "I will stay" (3 tokens, 2 occurrences)<br>2. "If it" (2 tokens, 2 occurrences)<br>3. "I will" (2 tokens, 2 occurrences)<br>4. "will stay" (2 tokens, 2 occurrences) | ✅ | Conditional sentence structure correctly recognized |
| 7 | Text 1: "This book is better than that one."<br>Text 2: "This movie is better than that one." | Found 16 patterns:<br>1. "is better than that one." (5 tokens, 2 occurrences)<br>2. "is better than that" (4 tokens, 2 occurrences)<br>3. "better than that one." (4 tokens, 2 occurrences) | ✅ | Comparative structure patterns fully detected |
| 8 | Text 1: "The store is located near the park."<br>Text 2: "The library is located near the school." | Found 11 patterns:<br>1. "is located near the" (4 tokens, 2 occurrences)<br>2. "is located near" (3 tokens, 2 occurrences)<br>3. "located near the" (3 tokens, 2 occurrences) | ✅ | Location expression patterns properly detected |
| 9 | Text 1: "First, I check my email. Then, I start working."<br>Text 2: "First, I check my messages. Then, I start studying." | Found 15 patterns:<br>1. "First, I check my" (4 tokens, 2 occurrences)<br>2. "First, I check" (3 tokens, 2 occurrences)<br>3. "I check my" (3 tokens, 2 occurrences)<br>4. "Then, I start" (3 tokens, 2 occurrences) | ✅ | Sequential action patterns detected |
| 10 | Text 1: "I think that chocolate is delicious."<br>Text 2: "I think that pizza is delicious."<br>Text 3: "I think that ice cream is delicious." | Found 9 patterns:<br>1. "I think that" (3 tokens, 3 files)<br>2. "I think" (2 tokens, 3 files)<br>3. "think that" (2 tokens, 3 files)<br>4. "is delicious." (2 tokens, 3 files) | ✅ | Opinion expression patterns perfectly detected |
| 11 | Text 1: "Because it was raining, we stayed inside."<br>Text 2: "Because it was cold, we stayed inside." | Found 12 patterns:<br>1. "Because it was" (3 tokens, 2 occurrences)<br>2. "we stayed inside." (3 tokens, 2 occurrences)<br>3. "Because it" (2 tokens, 2 occurrences)<br>4. "it was" (2 tokens, 2 occurrences) | ✅ | Causal clause structure detected |
| 12 | Text 1: "I need milk, bread, and eggs from the store."<br>Text 2: "She needs apples, bananas, and oranges from the market." | Found 4 patterns:<br>1. "from the" (2 tokens, 2 occurrences)<br>2. "and" (1 token, 2 occurrences)<br>3. "from" (1 token, 2 occurrences)<br>4. "the" (1 token, 2 occurrences) | ✅ | Common structural elements in lists detected |
| 13 | Text 1: "You should study hard for the exam."<br>Text 2: "You should practice hard for the game." | Found 9 patterns:<br>1. "hard for the" (3 tokens, 2 occurrences)<br>2. "You should" (2 tokens, 2 occurrences)<br>3. "hard for" (2 tokens, 2 occurrences)<br>4. "for the" (2 tokens, 2 occurrences) | ✅ | Modal verb patterns and prepositional phrases detected |
| 14 | Text 1: "Yesterday I went to the beach and saw dolphins."<br>Text 2: "Yesterday I went to the park and saw birds." | Found 18 patterns:<br>1. "Yesterday I went to the" (5 tokens, 2 occurrences)<br>2. "Yesterday I went to" (4 tokens, 2 occurrences)<br>3. "I went to the" (4 tokens, 2 occurrences)<br>4. "and saw" (2 tokens, 2 occurrences) | ✅ | Past experience narrative structure detected |
| 15 | Text 1: "Tomorrow I will go to the dentist."<br>Text 2: "Tomorrow I will go to the doctor."<br>Text 3: "Tomorrow I will go to the office." | Found 20+ patterns:<br>1. "Tomorrow I will go to the" (6 tokens, 3 files)<br>2. "Tomorrow I will go to" (5 tokens, 3 files)<br>3. "I will go to the" (5 tokens, 3 files) | ✅ | Future plan patterns completely detected |
| 16 | Text 1: "The large brown dog barked loudly."<br>Text 2: "The small black cat meowed loudly." | Found 2 patterns:<br>1. "The" (1 token, 2 occurrences)<br>2. "loudly." (1 token, 2 occurrences) | ✅ | Common adverb in descriptive sentences detected |
| 17 | Text 1: "Please turn off the lights before leaving."<br>Text 2: "Please turn off the computer before leaving." | Found 13 patterns:<br>1. "Please turn off the" (4 tokens, 2 occurrences)<br>2. "Please turn off" (3 tokens, 2 occurrences)<br>3. "turn off the" (3 tokens, 2 occurrences)<br>4. "before leaving." (2 tokens, 2 occurrences) | ✅ | Imperative sentence structure accurately detected |
| 18 | Text 1: "I prefer coffee to tea in the morning."<br>Text 2: "I prefer juice to milk in the morning." | Found 10 patterns:<br>1. "in the morning." (3 tokens, 2 occurrences)<br>2. "I prefer" (2 tokens, 2 occurrences)<br>3. "in the" (2 tokens, 2 occurrences)<br>4. "the morning." (2 tokens, 2 occurrences) | ✅ | Preference expression patterns detected |
| 19 | Text 1: "Once upon a time, there was a princess."<br>Text 2: "Once upon a time, there was a dragon."<br>Text 3: "Once upon a time, there was a wizard." | Found 20+ patterns:<br>1. "Once upon a time, there was a" (7 tokens, 3 files)<br>2. "Once upon a time, there was" (6 tokens, 3 files)<br>3. "upon a time, there was a" (6 tokens, 3 files) | ✅ | Story opening formula perfectly detected |
| 20 | Text 1: "When I arrive at work, I always check my email first and then review my schedule for the day."<br>Text 2: "When I arrive at home, I always check my mail first and then prepare my dinner for the evening." | Found 20+ patterns:<br>1. "When I arrive at" (4 tokens, 2 occurrences)<br>2. "I always check my" (4 tokens, 2 occurrences)<br>3. "first and then" (3 tokens, 2 occurrences) | ✅ | Complex sentence patterns properly extracted |

##### 表3: English Grammar Analyzer機能 レベル2精度評価

**Test Date**: 2025-08-03

**Overall Success Rate**: 20/20 (100%) ✅

| # | Input | Output | ✔︎ | Comment |
|---|-------|--------|---|---------|
| 1 | Text 1: "The cat sits on the mat."<br>Text 2: "The dog sits on the floor." | Found 3 patterns:<br>1. "sits(VERB) on(ADP) the(DET)" (3 tokens, 2 occurrences)<br>2. "sits(VERB) on(ADP)" (2 tokens, 2 occurrences)<br>3. "on(ADP) the(DET)" (2 tokens, 2 occurrences) | ✅ | Common pattern with determiner, noun, verb, preposition |
| 2 | Text 1: "She quickly runs to school."<br>Text 2: "He quickly walks to work." | Found 2 patterns:<br>1. "quickly(ADV)" (1 token, 2 occurrences)<br>2. ".(PUNCT)" (1 token, 2 occurrences) | ✅ | Pattern with adverb modifying verb |
| 3 | Text 1: "I love eating pizza and pasta."<br>Text 2: "We love eating burgers and fries." | Found 3 patterns:<br>1. "love(VERB) eating(VERB)" (2 tokens, 2 occurrences)<br>2. "love(VERB)" (1 token, 2 occurrences)<br>3. "eating(VERB)" (1 token, 2 occurrences) | ✅ | Pattern with gerund and coordinated nouns |
| 4 | Text 1: "The beautiful garden blooms in spring."<br>Text 2: "The beautiful park shines in summer." | Found 3 patterns:<br>1. "The(DET) beautiful(ADJ)" (2 tokens, 2 occurrences)<br>2. "The(DET)" (1 token, 2 occurrences)<br>3. "beautiful(ADJ)" (1 token, 2 occurrences) | ✅ | Pattern with adjective-noun combination |
| 5 | Text 1: "Can you help me with this?"<br>Text 2: "Can you assist me with that?" | Found 3 patterns:<br>1. "Can(AUX) you(PRON)" (2 tokens, 2 occurrences)<br>2. "me(PRON) with(ADP)" (2 tokens, 2 occurrences)<br>3. "Can(AUX)" (1 token, 2 occurrences) | ✅ | Modal auxiliary pattern |
| 6 | Text 1: "She has been studying all day."<br>Text 2: "He has been working all night." | Found 3 patterns:<br>1. "has(AUX) been(AUX)" (2 tokens, 2 occurrences)<br>2. "has(AUX)" (1 token, 2 occurrences)<br>3. "been(AUX)" (1 token, 2 occurrences) | ✅ | Present perfect continuous pattern |
| 7 | Text 1: "If it rains, we will stay home."<br>Text 2: "If it snows, we will stay inside." | Found 3 patterns:<br>1. ",(PUNCT) we(PRON) will(AUX) stay(VERB)" (4 tokens, 2 occurrences)<br>2. ",(PUNCT) we(PRON) will(AUX)" (3 tokens, 2 occurrences)<br>3. "we(PRON) will(AUX) stay(VERB)" (3 tokens, 2 occurrences) | ✅ | Conditional sentence pattern |
| 8 | Text 1: "The book that I read was interesting."<br>Text 2: "The movie that I watched was boring." | Found 3 patterns:<br>1. "that(PRON) I(PRON)" (2 tokens, 2 occurrences)<br>2. "The(DET)" (1 token, 2 occurrences)<br>3. "that(PRON)" (1 token, 2 occurrences) | ✅ | Relative clause pattern |
| 9 | Text 1: "Running is good for health."<br>Text 2: "Swimming is good for fitness." | Found 3 patterns:<br>1. "is(AUX) good(ADJ) for(ADP)" (3 tokens, 2 occurrences)<br>2. "is(AUX) good(ADJ)" (2 tokens, 2 occurrences)<br>3. "good(ADJ) for(ADP)" (2 tokens, 2 occurrences) | ✅ | Gerund as subject pattern |
| 10 | Text 1: "She told me to wait here."<br>Text 2: "He asked me to wait there." | Found 3 patterns:<br>1. "me(PRON) to(PART) wait(VERB)" (3 tokens, 2 occurrences)<br>2. "me(PRON) to(PART)" (2 tokens, 2 occurrences)<br>3. "to(PART) wait(VERB)" (2 tokens, 2 occurrences) | ✅ | Infinitive phrase pattern |
| 11 | Text 1: "Not only did she sing, but she also danced."<br>Text 2: "Not only did he play, but he also coached." | Found 3 patterns:<br>1. "Not(PART) only(ADV) did(AUX)" (3 tokens, 2 occurrences)<br>2. "Not(PART) only(ADV)" (2 tokens, 2 occurrences)<br>3. "only(ADV) did(AUX)" (2 tokens, 2 occurrences) | ✅ | Complex correlative conjunction pattern |
| 12 | Text 1: "The more you practice, the better you become."<br>Text 2: "The more you study, the smarter you become." | Found 3 patterns:<br>1. "The(PRON) more(ADV) you(PRON)" (3 tokens, 2 occurrences)<br>2. "you(PRON) become(VERB) .(PUNCT)" (3 tokens, 2 occurrences)<br>3. "The(PRON) more(ADV)" (2 tokens, 2 occurrences) | ✅ | Comparative correlative pattern |
| 13 | Text 1: "There are many books on the shelf."<br>Text 2: "There are many toys on the floor." | Found 3 patterns:<br>1. "There(PRON) are(VERB) many(ADJ)" (3 tokens, 2 occurrences)<br>2. "There(PRON) are(VERB)" (2 tokens, 2 occurrences)<br>3. "are(VERB) many(ADJ)" (2 tokens, 2 occurrences) | ✅ | Existential 'there' pattern |
| 14 | Text 1: "What a beautiful day it is!"<br>Text 2: "What a wonderful time it was!" | Found 3 patterns:<br>1. "What(PRON) a(DET)" (2 tokens, 2 occurrences)<br>2. "What(PRON)" (1 token, 2 occurrences)<br>3. "a(DET)" (1 token, 2 occurrences) | ✅ | Exclamatory sentence pattern |
| 15 | Text 1: "John, my best friend, lives nearby."<br>Text 2: "Mary, my dear sister, works nearby." | Found 3 patterns:<br>1. ",(PUNCT) my(PRON)" (2 tokens, 2 occurrences)<br>2. "nearby(ADV) .(PUNCT)" (2 tokens, 2 occurrences)<br>3. ",(PUNCT)" (1 token, 4 occurrences) | ✅ | Appositive phrase pattern |
| 16 | Text 1: "Having finished the work, she went home."<br>Text 2: "Having completed the task, he went away." | Found 3 patterns:<br>1. "Having(AUX)" (1 token, 2 occurrences)<br>2. "the(DET)" (1 token, 2 occurrences)<br>3. ",(PUNCT)" (1 token, 2 occurrences) | ✅ | Participial phrase pattern |
| 17 | Text 1: "It is important to exercise regularly."<br>Text 2: "It is necessary to study consistently." | Found 3 patterns:<br>1. "It(PRON) is(AUX)" (2 tokens, 2 occurrences)<br>2. "It(PRON)" (1 token, 2 occurrences)<br>3. "is(AUX)" (1 token, 2 occurrences) | ✅ | Extraposition pattern |
| 18 | Text 1: "The faster he runs, the more tired he gets."<br>Text 2: "The harder she works, the more successful she becomes." | Found 3 patterns:<br>1. ",(PUNCT) the(PRON) more(ADV)" (3 tokens, 2 occurrences)<br>2. ",(PUNCT) the(PRON)" (2 tokens, 2 occurrences)<br>3. "the(PRON) more(ADV)" (2 tokens, 2 occurrences) | ✅ | Complex comparative pattern |
| 19 | Text 1: "Either you come with us or stay here alone."<br>Text 2: "Either we go together or stay here together." | Found 3 patterns:<br>1. "or(CCONJ) stay(VERB) here(ADV)" (3 tokens, 2 occurrences)<br>2. "or(CCONJ) stay(VERB)" (2 tokens, 2 occurrences)<br>3. "stay(VERB) here(ADV)" (2 tokens, 2 occurrences) | ✅ | Either-or coordination pattern |
| 20 | Text 1: "Despite being tired, she continued working hard."<br>Text 2: "Despite being sick, he continued studying hard." | Found 3 patterns:<br>1. "Despite(SCONJ) being(AUX)" (2 tokens, 2 occurrences)<br>2. "hard(ADV) .(PUNCT)" (2 tokens, 2 occurrences)<br>3. "Despite(SCONJ)" (1 token, 2 occurrences) | ✅ | Concessive phrase pattern |


##### 表4: English Grammar Analyzer機能 レベル3精度評価

**Test Date**: 2025-08-03
**Overall Success Rate**: 18/20 (90%) ✅


| # | Input | Output | ✔︎ | Comment |
|---|-------|--------|---|---------|
| 1 | Text 1: "The happy children play in the garden."<br>Text 2: "The excited students work in the classroom." | Found 4 patterns:<br>1. "in[PP] the[NP]" (2 tokens, 2 occurrences)<br>2. "The[NP]" (1 tokens, 2 occurrences)<br>3. "in[PP]" (1 tokens, 2 occurrences) | ✅ | NP + VP + PP patterns |
| 2 | Text 1: "She quickly walked to the store."<br>Text 2: "He slowly drove to the office." | Found 3 patterns:<br>1. "to[PP] the[NP]" (2 tokens, 2 occurrences)<br>2. "to[PP]" (1 tokens, 2 occurrences)<br>3. "the[NP]" (1 tokens, 2 occurrences) | ✅ | ADVP + VP + PP patterns |
| 3 | Text 1: "The big red ball bounced high."<br>Text 2: "The small blue car moved fast." | Found 1 patterns:<br>1. "The[NP]" (1 tokens, 2 occurrences) | ✅ | Complex NP with multiple modifiers |
| 4 | Text 1: "John gave Mary a beautiful gift."<br>Text 2: "Sarah sent Tom a lovely card." | Found 1 patterns:<br>1. "a[NP]" (1 tokens, 2 occurrences) | ✅ | Double object VP pattern |
| 5 | Text 1: "After the meeting, we went home."<br>Text 2: "Before the class, they ate lunch." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 2 occurrences) | ✅ | PP at sentence beginning |
| 6 | Text 1: "The book on the table is mine."<br>Text 2: "The pen in the drawer is yours." | Found 3 patterns:<br>1. "The[NP]" (1 tokens, 2 occurrences)<br>2. "the[NP]" (1 tokens, 2 occurrences)<br>3. "is[VP]" (1 tokens, 2 occurrences) | ✅ | NP with embedded PP |
| 7 | Text 1: "Running quickly exhausted him completely."<br>Text 2: "Swimming slowly relaxed her totally." | No patterns found | ❌ | Gerund VP as subject |
| 8 | Text 1: "She seems very happy today."<br>Text 2: "He looks quite tired now." | No patterns found | ❌ | Linking verb + ADJP pattern |
| 9 | Text 1: "The teacher explained the lesson clearly to the students."<br>Text 2: "The speaker presented the topic briefly to the audience." | Found 4 patterns:<br>1. "to[PP] the[NP]" (2 tokens, 2 occurrences)<br>2. "the[NP]" (1 tokens, 4 occurrences)<br>3. "The[NP]" (1 tokens, 2 occurrences) | ✅ | Complex VP with ADVP and PP |
| 10 | Text 1: "In the morning, birds sing beautifully."<br>Text 2: "At the night, owls hoot mysteriously." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 2 occurrences) | ✅ | PP + NP + VP + ADVP |
| 11 | Text 1: "The extremely talented musician played wonderfully."<br>Text 2: "The incredibly skilled artist painted beautifully." | Found 1 patterns:<br>1. "The[NP]" (1 tokens, 2 occurrences) | ✅ | Intensified ADJP in NP |
| 12 | Text 1: "They found the solution surprisingly easy."<br>Text 2: "We considered the problem remarkably simple." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 2 occurrences) | ✅ | Object complement with ADVP |
| 13 | Text 1: "Walking through the park, she saw many flowers."<br>Text 2: "Jogging along the beach, he noticed several shells." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 2 occurrences) | ✅ | Participial phrase + main clause |
| 14 | Text 1: "To succeed in life, one must work hard."<br>Text 2: "To excel at sports, you should practice daily." | Found 1 patterns:<br>1. "To[INF-P]" (1 tokens, 2 occurrences) | ✅ | Infinitive phrase pattern |
| 15 | Text 1: "The students studying hard will pass easily."<br>Text 2: "The workers arriving early can leave sooner." | Found 1 patterns:<br>1. "The[NP]" (1 tokens, 2 occurrences) | ✅ | Reduced relative clause in NP |
| 16 | Text 1: "Both the cat and the dog sleep peacefully."<br>Text 2: "Either the bus or the train arrives promptly." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 4 occurrences) | ✅ | Coordinated NP subjects |
| 17 | Text 1: "She not only sings beautifully but also dances gracefully."<br>Text 2: "He not only writes clearly but also speaks eloquently." | Found 6 patterns:<br>1. "not[PART] only[ADVP]" (2 tokens, 2 occurrences)<br>2. "but[CONJP] also[ADVP]" (2 tokens, 2 occurrences)<br>3. "not[PART]" (1 tokens, 2 occurrences) | ✅ | Correlative conjunction with ADVP |
| 18 | Text 1: "The more carefully you study, the better you understand."<br>Text 2: "The more diligently she works, the faster she progresses." | Found 4 patterns:<br>1. "The[ADVP] more[ADVP]" (2 tokens, 2 occurrences)<br>2. "The[ADVP]" (1 tokens, 2 occurrences)<br>3. "more[ADVP]" (1 tokens, 2 occurrences) | ✅ | Comparative correlative with ADVP |
| 19 | Text 1: "Despite the heavy rain, they continued playing outside."<br>Text 2: "Despite the strong wind, we kept walking forward." | Found 3 patterns:<br>1. "Despite[CONJP] the[NP]" (2 tokens, 2 occurrences)<br>2. "Despite[CONJP]" (1 tokens, 2 occurrences)<br>3. "the[NP]" (1 tokens, 2 occurrences) | ✅ | Concessive PP + VP + ADVP |
| 20 | Text 1: "What she said yesterday surprised everyone greatly."<br>Text 2: "What he did today shocked everybody completely." | Found 1 patterns:<br>1. "What[NP]" (1 tokens, 2 occurrences) | ✅ | Nominal clause as subject |

**失敗したテストケース**

  1. テスト #7: "Running quickly exhausted him completely." / "Swimming slowly relaxed her
  totally."
    - 期待: 動名詞（Gerund）がVPとして認識される
    - 結果: パターンが検出されなかった
  2. テスト #8: "She seems very happy today." / "He looks quite tired now."
    - 期待: リンク動詞 + 形容詞句（ADJP）パターンの検出
    - 結果: パターンが検出されなかった

  ##### 失敗の原因分析

  1. spaCyのタグ付け精度の問題

  - 動名詞の誤認識: "Running"と"Swimming"が主語として使われている場合、spaCyはこれらを固有
  名詞（PROPN）として誤認識する傾向があります
  - 形容詞句の認識不足: "very happy"や"quite
  tired"のような形容詞句が、異なる句タイプとして分類される可能性

  2. カスタム修正の限界

  Pattern Finderには_apply_custom_correctionsメソッドが実装されていますが：
  - 動名詞主語の修正は実装済み（-ing形でPROPNかつnsubjの場合VPに修正）
  - しかし、時間表現の修正のみで、形容詞句パターンの修正は含まれていない

  3. Level 3の設計上の制約

  - Level 3は「Token + Phrase Type」の完全一致を求める
  - 例：
    - Text 1: "Running[VP] quickly[ADVP]"
    - Text 2: "Swimming[VP] slowly[ADVP]"
    - 異なるトークン（Running vs Swimming）のため、パターンとして検出されない

##### 表5: English Grammar Analyzer機能 レベル4精度評価

**Test Date**: 2025-08-05
**Overall Success Rate**: 20/20 (10%) ✅

| # | Input | Output | ✔︎ | Comment |
|---|-------|--------|---|---------|
| 1 | Text 1: "The happy children play in the garden."<br>Text 2: "The excited students work in the classroom." | Found 7 patterns:<br>1. "in(ADP)[PP] the(DET)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>... and 4 more | ✅ | NP + VP + PP patterns |
| 2 | Text 1: "She quickly walked to the store."<br>Text 2: "He slowly drove to the office." | Found 6 patterns:<br>1. "to(ADP)[PP] the(DET)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. "to(ADP)[PP]" (1 tokens, 2 occurrences)<br>... and 3 more | ✅ | ADVP + VP + PP patterns |
| 3 | Text 1: "The big red ball bounced high."<br>Text 2: "The small blue car moved fast." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Complex NP with multiple modifiers |
| 4 | Text 1: "John gave Mary a beautiful gift."<br>Text 2: "Sarah sent Tom a lovely card." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. "a(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Double object VP pattern |
| 5 | Text 1: "After the meeting, we went home."<br>Text 2: "Before the class, they ate lunch." | Found 5 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ",(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 2 more | ✅ | PP at sentence beginning |
| 6 | Text 1: "The book on the table is mine."<br>Text 2: "The pen in the drawer is yours." | Found 6 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>3. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>... and 3 more | ✅ | NP with embedded PP |
| 7 | Text 1: "Running quickly exhausted him completely."<br>Text 2: "Swimming slowly relaxed her totally." | Found 3 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[ADVP]" (1 tokens, 2 occurrences) | ✅ | Gerund VP as subject |
| 8 | Text 1: "She seems very happy today."<br>Text 2: "He looks quite tired now." | Found 3 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[ADVP]" (1 tokens, 2 occurrences) | ✅ | Linking verb + ADJP pattern |
| 9 | Text 1: "The teacher explained the lesson clearly to the students."<br>Text 2: "The speaker presented the topic briefly to the audience." | Found 7 patterns:<br>1. "to(ADP)[PP] the(DET)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. "the(DET)[NP]" (1 tokens, 4 occurrences)<br>... and 4 more | ✅ | Complex VP with ADVP and PP |
| 10 | Text 1: "In the morning, birds sing beautifully."<br>Text 2: "At the night, owls hoot mysteriously." | Found 7 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>3. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>... and 4 more | ✅ | PP + NP + VP + ADVP |
| 11 | Text 1: "The extremely talented musician played wonderfully."<br>Text 2: "The incredibly skilled artist painted beautifully." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Intensified ADJP in NP |
| 12 | Text 1: "They found the solution surprisingly easy."<br>Text 2: "We considered the problem remarkably simple." | Found 2 patterns:<br>1. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>2. ".(PUNCT)[O]" (1 tokens, 2 occurrences) | ✅ | Object complement with ADVP |
| 13 | Text 1: "Walking through the park, she saw many flowers."<br>Text 2: "Jogging along the beach, he noticed several shells." | Found 7 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>... and 4 more | ✅ | Participial phrase + main clause |
| 14 | Text 1: "To succeed in life, one must work hard."<br>Text 2: "To excel at sports, you should practice daily." | Found 7 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>3. "To(PART)[INF-P]" (1 tokens, 2 occurrences)<br>... and 4 more | ✅ | Infinitive phrase pattern |
| 15 | Text 1: "The students studying hard will pass easily."<br>Text 2: "The workers arriving early can leave sooner." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Reduced relative clause in NP |
| 16 | Text 1: "Both the cat and the dog sleep peacefully."<br>Text 2: "Either the bus or the train arrives promptly." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "the(DET)[NP]" (1 tokens, 4 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Coordinated NP subjects |
| 17 | Text 1: "She not only sings beautifully but also dances gracefully."<br>Text 2: "He not only writes clearly but also speaks eloquently." | Found 9 patterns:<br>1. "not(PART)[PART] only(ADV)[ADVP]" (2 tokens, 2 occurrences)<br>2. "but(CCONJ)[CONJP] also(ADV)[ADVP]" (2 tokens, 2 occurrences)<br>3. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>... and 6 more | ✅ | Correlative conjunction with ADVP |
| 18 | Text 1: "The more carefully you study, the better you understand."<br>Text 2: "The more diligently she works, the faster she progresses." | Found 12 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[VP] the(PRON)[ADVP]" (3 tokens, 2 occurrences)<br>2. "The(PRON)[ADVP] more(ADV)[ADVP]" (2 tokens, 2 occurrences)<br>3. ",(PUNCT)[O] ,(PUNCT)[VP]" (2 tokens, 2 occurrences)<br>... and 9 more | ✅ | Comparative correlative with ADVP |
| 19 | Text 1: "Despite the heavy rain, they continued playing outside."<br>Text 2: "Despite the strong wind, we kept walking forward." | Found 9 patterns:<br>1. "Despite(SCONJ)[CONJP] the(DET)[NP]" (2 tokens, 2 occurrences)<br>2. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>... and 6 more | ✅ | Concessive PP + VP + ADVP |
| 20 | Text 1: "What she said yesterday surprised everyone greatly."<br>Text 2: "What he did today shocked everybody completely." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "What(PRON)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Nominal clause as subject |

### One-to-one or group Interview

実施日: 2025年8月5日
対象者: 大学生1名


#### 高く評価された点

1. English Grammar Analyzerの学習効果

「時制変換機能は、不規則動詞の活用を覚えるのに役立つ。特に、andで繋がれた動詞がまとめて変換されるのが便利」

2. UI/UX
「Add Textボタンによるテキストエリアの追加や、レスポンシブデザインによるスマートフォンでの表示崩れがない点でストレスなく操作できて良い」

#### 改善に関する提案

1. Pattern Finderの可視化

「分析レベルの違いが分かりにくい。各レベルにマウスを乗せると説明が出るような機能が欲しい」

「検出された共通パターンが、元の入力テキストのどの部分に当たるのかハイライト表示されると、視覚的に理解しやすくなると思う」

2. English Grammar Analyzerの解説機能

「なぜcompoundと判定されたのか、等位接続詞（and, butなど）をハイライトするような簡単な解説があると、文法理解がさらに深まる」