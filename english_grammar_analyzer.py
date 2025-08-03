import spacy
import json
from typing import List, Dict, Tuple


class EnglishGrammarAnalyzer:
    def __init__(self):
        """
        English Grammar Analyzerの初期化
        spaCyモデルをロードし、過去形変換辞書を準備
        """
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except IOError:
            raise Exception("spaCy English model not found. Please run: python -m spacy download en_core_web_sm")
        
        # 不規則動詞の過去形辞書
        self.irregular_verbs = {
            'am': 'was', 'is': 'was', 'are': 'were', 'be': 'was', 'been': 'was',
            'have': 'had', 'has': 'had', 'do': 'did', 'does': 'did',
            'go': 'went', 'goes': 'went', 'come': 'came', 'comes': 'came',
            'get': 'got', 'gets': 'got', 'take': 'took', 'takes': 'took',
            'make': 'made', 'makes': 'made', 'see': 'saw', 'sees': 'saw',
            'know': 'knew', 'knows': 'knew', 'think': 'thought', 'thinks': 'thought',
            'give': 'gave', 'gives': 'gave', 'find': 'found', 'finds': 'found',
            'tell': 'told', 'tells': 'told', 'become': 'became', 'becomes': 'became',
            'leave': 'left', 'leaves': 'left', 'feel': 'felt', 'feels': 'felt',
            'bring': 'brought', 'brings': 'brought', 'begin': 'began', 'begins': 'began',
            'keep': 'kept', 'keeps': 'kept', 'hold': 'held', 'holds': 'held',
            'write': 'wrote', 'writes': 'wrote', 'stand': 'stood', 'stands': 'stood',
            'hear': 'heard', 'hears': 'heard', 'let': 'let', 'lets': 'let',
            'mean': 'meant', 'means': 'meant', 'set': 'set', 'sets': 'set',
            'meet': 'met', 'meets': 'met', 'run': 'ran', 'runs': 'ran',
            'pay': 'paid', 'pays': 'paid', 'sit': 'sat', 'sits': 'sat',
            'speak': 'spoke', 'speaks': 'spoke', 'lie': 'lay', 'lies': 'lay',
            'lead': 'led', 'leads': 'led', 'read': 'read', 'reads': 'read',
            'grow': 'grew', 'grows': 'grew', 'lose': 'lost', 'loses': 'lost',
            'send': 'sent', 'sends': 'sent', 'build': 'built', 'builds': 'built',
            'understand': 'understood', 'understands': 'understood',
            'draw': 'drew', 'draws': 'drew', 'break': 'broke', 'breaks': 'broke',
            'spend': 'spent', 'spends': 'spent', 'cut': 'cut', 'cuts': 'cut',
            'rise': 'rose', 'rises': 'rose', 'drive': 'drove', 'drives': 'drove',
            'buy': 'bought', 'buys': 'bought', 'wear': 'wore', 'wears': 'wore',
            'choose': 'chose', 'chooses': 'chose', 'fall': 'fell', 'falls': 'fell',
            'fly': 'flew', 'flies': 'flew', 'forget': 'forgot', 'forgets': 'forgot',
            'eat': 'ate', 'eats': 'ate', 'drink': 'drank', 'drinks': 'drank',
            'sing': 'sang', 'sings': 'sang', 'swim': 'swam', 'swims': 'swam',
            'ring': 'rang', 'rings': 'rang', 'win': 'won', 'wins': 'won',
            'throw': 'threw', 'throws': 'threw', 'catch': 'caught', 'catches': 'caught',
            'teach': 'taught', 'teaches': 'taught', 'sleep': 'slept', 'sleeps': 'slept',
            'fight': 'fought', 'fights': 'fought', 'sell': 'sold', 'sells': 'sold',
            'shine': 'shone', 'shines': 'shone',
            'can': 'could', 'will': 'would', 'shall': 'should',
            'may': 'might', 'must': 'had to'
        }

    def convert_to_past_tense(self, text: str) -> str:
        """
        文章内のすべての動詞を過去形に変換
        """
        doc = self.nlp(text)
        tokens = []
        
        for token in doc:
            if self._should_convert_to_past(token, doc):
                # 動詞を過去形に変換
                past_form = self._get_past_form(token)
                tokens.append(past_form)
            else:
                tokens.append(token.text)
        
        # スペースとトークンを適切に結合（修正版）
        result = ""
        for i, token in enumerate(doc):
            if i > 0 and not token.is_punct:
                result += " "
            result += tokens[i]
        
        return result

    def _should_convert_to_past(self, token, doc) -> bool:
        """
        トークンが過去形に変換すべき動詞かどうかを判定
        等位接続詞で結ばれた動詞や誤ったタグ付けにも対応
        """
        # 基本的な動詞チェック
        if token.pos_ not in ['VERB', 'AUX']:
            return False
        
        # 既に過去形の動詞は変換しない
        if token.tag_ == 'VBD':
            return False
        
        # 助動詞の処理
        if token.pos_ == 'AUX':
            # 助動詞（can, will, may等）は過去形に変換
            if token.tag_ == 'MD':  # Modal auxiliary
                return True
            # be動詞（is, are, am等）も変換対象
            if token.lemma_ == 'be':
                return True
            # have動詞（has, have等）も変換対象
            if token.lemma_ == 'have':
                return True
            return False
        
        # 助動詞に続く動詞は原形のままにする
        if self._follows_modal_auxiliary(token, doc):
            return False
        
        # 特別なケース: 等位接続詞で結ばれた動詞の処理
        # "swim, run, and fly" のような構造での動詞検出
        if token.tag_ == 'VBN':
            # 過去分詞タグでも、等位接続詞の文脈では原形動詞の可能性
            if self._is_coordinated_verb(token, doc):
                return True
            # 受動態やperfect tenseでない場合は原形動詞として扱う
            if not self._is_passive_or_perfect(token, doc):
                return True
        
        # VBG（-ing形）の特別処理：現在進行形では変換しない
        if token.tag_ == 'VBG':
            # 現在進行形（be動詞 + -ing形）の文脈では変換しない
            if self._is_progressive_tense(token, doc):
                return False
            return True
        
        # その他の動詞形式（VB, VBP, VBZ）は変換対象
        if token.tag_ in ['VB', 'VBP', 'VBZ']:
            return True
        
        return False

    def _is_progressive_tense(self, token, doc) -> bool:
        """
        VBGトークンが現在進行形（be動詞 + -ing形）の文脈にあるかを判定
        """
        if token.tag_ != 'VBG':
            return False
        
        # VBGトークンの依存関係をチェック
        # 現在進行形では、be動詞がauxとしてVBGに依存
        for child in token.children:
            if child.pos_ == 'AUX' and child.dep_ == 'aux' and child.lemma_ == 'be':
                return True
        
        return False

    def _follows_modal_auxiliary(self, token, doc) -> bool:
        """
        動詞が助動詞（can, will, may等）に直接続くかどうかを判定
        """
        for i, t in enumerate(doc):
            if t == token:
                # 直前のトークンが助動詞かチェック
                if i > 0:
                    prev_token = doc[i-1]
                    if prev_token.pos_ == 'AUX' and prev_token.tag_ == 'MD':
                        return True
                # さらに前のトークンも確認（代名詞等が間にある場合）
                if i > 1:
                    prev_prev_token = doc[i-2]
                    if prev_prev_token.pos_ == 'AUX' and prev_prev_token.tag_ == 'MD':
                        return True
                break
        return False

    def _is_coordinated_verb(self, token, doc) -> bool:
        """
        等位接続詞（and, or等）で結ばれた動詞かどうかを判定
        """
        # 前の語句をチェックして等位接続詞があるかを確認
        for i, t in enumerate(doc):
            if t == token:
                # 前方の語句をチェック
                for j in range(max(0, i-5), i):
                    if doc[j].pos_ == 'CCONJ':  # 等位接続詞
                        return True
                break
        return False

    def _is_passive_or_perfect(self, token, doc) -> bool:
        """
        受動態またはperfect tenseの一部かどうかを判定
        """
        # 前の語句にbe動詞やhave動詞があるかチェック
        for i, t in enumerate(doc):
            if t == token:
                # 前の語句をチェック
                for j in range(max(0, i-3), i):
                    if doc[j].lemma_ in ['be', 'have', 'has', 'had', 'is', 'are', 'was', 'were']:
                        return True
                break
        return False

    def _get_past_form(self, token) -> str:
        """
        個別の動詞トークンを過去形に変換
        """
        lemma = token.lemma_.lower()
        text = token.text.lower()
        
        # 不規則動詞のチェック（具体的な形を優先）
        if text in self.irregular_verbs:
            past_form = self.irregular_verbs[text]
        elif lemma in self.irregular_verbs:
            past_form = self.irregular_verbs[lemma]
        else:
            # 規則動詞の過去形生成
            past_form = self._make_regular_past(lemma)
        
        # 元の大文字小文字を保持
        if token.text[0].isupper():
            past_form = past_form.capitalize()
        
        return past_form

    def _make_regular_past(self, verb: str) -> str:
        """
        規則動詞の過去形を生成
        """
        if verb.endswith('e'):
            return verb + 'd'
        elif verb.endswith('y') and len(verb) > 1 and verb[-2] not in 'aeiou':
            # 子音 + y の場合: study → studied
            return verb[:-1] + 'ied'
        elif verb.endswith('y'):
            # 母音 + y の場合: play → played (単純にedを追加)
            return verb + 'ed'
        elif len(verb) >= 3 and verb[-1] not in 'aeiou' and verb[-2] in 'aeiou' and verb[-3] not in 'aeiou':
            # CVC pattern (consonant-vowel-consonant) - double the last consonant
            # ただし、yで終わる単語は除外済み
            return verb + verb[-1] + 'ed'
        else:
            return verb + 'ed'

    def get_sentence_type(self, text: str) -> str:
        """
        文のタイプを判定（Simple, Compound, Complex）
        """
        doc = self.nlp(text)
        
        # 従属接続詞をチェック（Complex判定）
        subordinators = {
            'after', 'although', 'as', 'because', 'before', 'even if', 'even though',
            'if', 'once', 'since', 'so that', 'than', 'though', 'unless',
            'until', 'when', 'whenever', 'where', 'whereas', 'wherever', 'whether', 'while',
            'that'  # 関係代名詞のthatも含める
        }
        
        # 依存関係を使ってより正確に従属節を検出
        has_subordinate_clause = False
        for token in doc:
            if token.text.lower() in subordinators:
                # 従属接続詞が実際に従属節を導入しているかチェック
                if token.dep_ in ['mark', 'advmod', 'prep'] or any(child.dep_ in ['ccomp', 'advcl', 'acl'] for child in token.head.children):
                    has_subordinate_clause = True
                    break
        
        if has_subordinate_clause:
            return 'complex'
        
        # 等位接続詞をチェック（Compound判定）
        coordinate_conjunctions = {'and', 'but', 'or', 'nor', 'for', 'so', 'yet'}
        
        # 実際に独立節を結合している等位接続詞を検出
        has_coordinate_clause = False
        main_verbs = 0
        
        for token in doc:
            # 主要動詞をカウント
            if token.pos_ in ['VERB', 'AUX'] and token.dep_ in ['ROOT', 'conj']:
                main_verbs += 1
            
            # 等位接続詞をチェック
            if token.text.lower() in coordinate_conjunctions and token.dep_ == 'cc':
                has_coordinate_clause = True
        
        if has_coordinate_clause and main_verbs > 1:
            return 'compound'
        
        return 'simple'

    def get_prepositional_phrases(self, text: str) -> List[str]:
        """
        前置詞句を抽出（改良版）
        """
        doc = self.nlp(text)
        prep_phrases = []
        
        for token in doc:
            if token.pos_ == 'ADP':  # 前置詞
                phrase_tokens = [token]
                
                # 前置詞の目的語とその修飾語を収集
                for child in token.children:
                    if child.dep_ == 'pobj':  # 前置詞の目的語
                        phrase_tokens.extend(self._get_noun_phrase_tokens(child, doc))
                
                # 前置詞句が有効な場合のみ追加
                if len(phrase_tokens) > 1:  # 前置詞 + 少なくとも1語
                    # トークンを正しい順序でソート
                    phrase_tokens.sort(key=lambda x: x.i)
                    phrase_text = " ".join([t.text for t in phrase_tokens])
                    prep_phrases.append(phrase_text)
        
        # 重複を除去し、長い順にソート（より具体的な句を優先）
        prep_phrases = list(set(prep_phrases))
        prep_phrases.sort(key=len, reverse=True)
        
        return prep_phrases

    def _get_noun_phrase_tokens(self, head_token, doc) -> List:
        """
        名詞句の全トークンを取得（修飾語を含む）
        """
        tokens = [head_token]
        
        # 子要素を再帰的に収集
        for child in head_token.children:
            if child.dep_ in ['det', 'amod', 'compound', 'nummod', 'poss', 'prep', 'relcl', 'acl']:
                if child.dep_ == 'prep':
                    # 前置詞の場合、その目的語も含める
                    tokens.append(child)
                    for grandchild in child.children:
                        if grandchild.dep_ == 'pobj':
                            tokens.extend(self._get_noun_phrase_tokens(grandchild, doc))
                else:
                    tokens.extend(self._get_noun_phrase_tokens(child, doc))
        
        return tokens

    def analyze_text(self, text: str) -> Dict:
        """
        テキストの包括的な文法分析
        """
        if not text.strip():
            return {"error": "Text is empty"}
        
        try:
            # 過去形変換
            past_tense = self.convert_to_past_tense(text)
            
            # 文タイプ判定
            sentence_type = self.get_sentence_type(text)
            
            # 前置詞句抽出
            prep_phrases = self.get_prepositional_phrases(text)
            
            return {
                "original_text": text,
                "past_tense": past_tense,
                "sentence_type": sentence_type,
                "prepositional_phrases": prep_phrases,
                "success": True
            }
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}


def main():
    """
    コマンドライン実行用のメイン関数
    """
    analyzer = EnglishGrammarAnalyzer()
    
    print("English Grammar Analyzer (Python + spaCy)")
    print("Type 'quit' to exit\n")
    
    while True:
        text = input("Enter an English sentence: ").strip()
        
        if text.lower() == 'quit':
            break
        
        if not text:
            print("Please enter a valid sentence.\n")
            continue
        
        result = analyzer.analyze_text(text)
        
        if result.get("error"):
            print(f"Error: {result['error']}\n")
        else:
            print(f"Past tense: {result['past_tense']}")
            print(f"Sentence type: {result['sentence_type']}")
            print(f"Prepositional phrases: {', '.join(result['prepositional_phrases']) if result['prepositional_phrases'] else '(none)'}")
            print()


if __name__ == "__main__":
    main() 