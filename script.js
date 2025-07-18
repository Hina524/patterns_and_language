function convertToPast() {
  let text = document.getElementById('textInput').value;
  let output = document.getElementById('output');
  let loading = document.getElementById('loading');

  if (text.trim() === "") {
    output.innerText = "Please enter some text.";
    return;
  }

  loading.style.display = "inline-block";
  setTimeout(() => {
    let doc = nlp(text);
    let past = doc.sentences().toPastTense().text();
    // 文タイプ判定
    let type = getSentenceType(text);
    // 前置詞句の抽出
    let preps = getPrepositionalPhrases(text);
    let prepsText = preps.length > 0 ? preps.map(p => `- ${p}`).join("\n") : "(none)";
    output.innerText = `${past}\nsentence type: ${type}\nprepositional phrases: ${prepsText}`;
    loading.style.display = "none";
  }, 500);
}

// 文タイプ判定関数
function getSentenceType(text) {
const doc = nlp(text);
const lower = text.toLowerCase();

// 1. complex 判定（従属接続詞ベース）※ "that" は除外または構造解析を追加してもOK
const subordinators = [
  'after', 'although', 'as', 'because', 'before', 'even if', 'even though',
  'if', 'once', 'since', 'so that', 'than', 'though', 'unless',
  'until', 'when', 'whenever', 'where', 'whereas', 'wherever', 'whether', 'while'
];

for (let sub of subordinators) {
  if (
    sub !== 'that' && // ← 追加
    (lower.includes(' ' + sub + ' ') || lower.startsWith(sub + ' '))
  ) {
    return 'complex';
  }
}

// 2. compound 判定（前後に主語＋動詞がある and/but/or など）
if (isCompoundSentence(text)) {
  return 'compound';
}

// 3. 上記に該当しなければ simple
return 'simple';
}

//compound（重文）かどうかを判定する関数
function isCompoundSentence(text) {
const doc = nlp(text);
const sentences = doc.sentences().json();

// 単一文でない場合（複文など）、compoundとして扱わない
if (sentences.length !== 1) return false;

const terms = sentences[0].terms.map(term => ({
  text: term.text,
  pos: term.tags
}));

const conjunctions = ['and', 'but', 'or', 'nor', 'for', 'yet', 'so'];

// 探索：conjunctionの前後に主語＋動詞があるか
for (let i = 1; i < terms.length - 1; i++) {
  const curr = terms[i];
  if (conjunctions.includes(curr.text.toLowerCase())) {
    const left = terms.slice(0, i);
    const right = terms.slice(i + 1);
    if (hasSubjectVerb(left) && hasSubjectVerb(right)) {
      return true; // compound
    }
  }
}
return false;
}

// 主語と動詞の両方を含むかを判定する関数
function hasSubjectVerb(terms) {
let hasSubject = false;
let hasVerb = false;
for (const term of terms) {
  if (term.pos.includes('Pronoun') || term.pos.includes('Noun')) {
    hasSubject = true;
  }
  if (term.pos.includes('Verb')) {
    hasVerb = true;
  }
}
return hasSubject && hasVerb;
}

// 前置詞句抽出関数
function getPrepositionalPhrases(text) {
let doc = nlp(text);
let preps = [];
// Compromiseのchunkで前置詞句を抽出
let matches = doc.match('#Preposition .+? #Noun');
matches.forEach(m => {
  preps.push(m.text());
});
return preps;
}
