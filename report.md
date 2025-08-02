# English Learning Support Web Application
https://github.com/Hina524/patterns_and_language
# Group members

| 学籍番号     | 氏名           | 貢献内容                                           |
| -------- | ------------ | ---------------------------------------------- |
| s1310141 | Hina Konishi | 70% (main programmer, report, analysis) |
| s1290116 | Tsubasa Sato | 30% (analysis)                                 |
# **1. Tool description**
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
```javascript
let doc = nlp(text);
let past = doc.sentences().toPastTense().text();
```

**言語理論的基盤:**
- **英語動詞活用体系**: 規則動詞（-ed付加）・不規則動詞（語幹変化）の自動識別
- **時制一致原理**: 文全体における時制の統一性維持
- **compromise.js 形態論解析**: 語幹抽出→活用語尾処理→不規則動詞辞書照合
#### 2. 文構造分析
**理論的基盤: Traditional Grammar + Structural Linguistics**

1. **Simple Sentence（単文）**: 主語+動詞の基本構造
2. **Compound Sentence（重文）**: 等位接続詞による独立節結合
``` js
// 重文判定に使用する等位接続詞リスト
const conjunctions = ['and', 'but', 'or', 'nor', 'for', 'yet', 'so'];
```
1. **Complex Sentence（複文）**: 従属接続詞による主節+従属節構造
```javascript
// 複文判定に使用する従属接続詞リスト
const subordinators = [
    'after', 'although', 'as', 'because', 'before', 'even if', 'even though',
    'if', 'once', 'since', 'so that', 'than', 'though', 'unless',
    'until', 'when', 'whenever', 'where', 'whereas', 'wherever', 'whether', 'while'
];
```
#### 3. 前置詞句抽出
**統語論的パターンマッチング:**
```javascript
let matches = doc.match('#Preposition .+? #Noun');
```
- **構文パターン**: [前置詞] + [修飾語群] + [名詞]
- **句境界認識**: 非貪欲マッチング（.+?）による適切な境界検出
### Algorithm Diagram

``` mermaid
flowchart TD
    A[入力テキスト] --> B[compromise.js NLP処理]
    B --> C[文書オブジェクト生成]
    C --> D[時制変換処理]
    C --> E[文構造分析]
    C --> F[前置詞句抽出]
    
    D --> D1[動詞識別]
    D1 --> D2[規則/不規則判定]
    D2 --> D3[過去形変換]
    
    E --> E1[従属接続詞検索]
    E1 --> E2{従属接続詞存在?}
    E2 -->|Yes| E3[Complex判定]
    E2 -->|No| E4[等位接続詞分析]
    E4 --> E5{主語+動詞構造?}
    E5 -->|Yes| E6[Compound判定]
    E5 -->|No| E7[Simple判定]
    
    F --> F1[前置詞識別]
    F1 --> F2[修飾語範囲特定]
    F2 --> F3[名詞終端検出]
    F3 --> F4[前置詞句抽出]
    
    D3 --> G[結果統合]
    E3 --> G
    E6 --> G
    E7 --> G
    F4 --> G
    G --> H[出力表示]
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
    # Step 1: spaCy noun_chunksによる名詞句検出
    for chunk in doc.noun_chunks:
        for i in range(chunk.start, chunk.end):
            phrase_map[i] = 'NP'
    
    # Step 2: 依存関係解析による動詞句検出
    if token.pos_ in ['VERB', 'AUX'] and token.i not in phrase_map:
        vp_tokens = self._get_verb_phrase_tokens(token, doc)
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
    E --> E1[Step 1: 名詞句検出]
    E1 --> E2[Step 2: 動詞句検出]
    E2 --> E3[Step 3: 前置詞句検出]
    E3 --> E4[Step 4: 形容詞句検出]
    E4 --> E5[Step 5: 副詞句検出]
    E5 --> E6[Step 6: 残余トークン分類]
    
    subgraph "動詞句検出詳細"
        F1[動詞トークン特定]
        F2[依存関係解析]
        F3[aux/neg/prt検出]
        F4[不定詞to処理]
        F1 --> F2 --> F3 --> F4
    end
    
    E2 -.-> F1
    
    D1 --> G[トークン配列生成]
    D2 --> G
    E6 --> G
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
- **Python 3.11**
- **JavaScript ES6+**
- **HTML5**
- **CSS3**
### 主要ライブラリ
- **Flask 3.0.0**: 軽量Webフレームワーク
- **spaCy 3.8.5**: 産業標準NLPライブラリ
- **compromise.js**: クライアント側言語処理
- **W3.CSS**: レスポンシブCSSフレームワーク
## 
