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

// --- 追加: 各種テンプレート文リスト ---
const topicSentences = [
  'I want to describe a place called ___.',
  'My favorite ___ is ___.',
  'There is a special ___ that I often visit.',
  'Today, I will describe ___.',
  'One thing I really like is ___.',
  'I often go to ___ because it is ___.',
  'I always enjoy spending time at ___.',
  'The object I’m describing is something I use every day.',
  '___ is very meaningful to me.',
  'I have many memories of ___, so I want to describe it.'
];
const sensoryDetails = [
  'It looks ___ and ___.',
  'You can hear ___, especially when ___.',
  'The colors are ___, which makes it look ___.',
  'It smells like ___, and that reminds me of ___.',
  'It feels ___ when I touch it.',
  'You can see ___ all around.',
  'The sounds around it are usually ___.',
  'The texture is ___, soft and ___.',
  'The air smells like ___ on most days.',
  'It tastes like ___, which makes me feel ___.'
];
const spatialDetails = [
  'It is located near ___.',
  'Around it, there are ___ and ___.',
  'Inside, you can find ___.',
  'On the left side, you can see ___.',
  'Next to it, there is ___.',
  'People often come here to ___.',
  'The area is always ___ and ___.',
  'The place is usually quiet except when ___.',
  'From this spot, you can see ___ in the distance.',
  'There are many things placed around it, such as ___.'
];
const concludingSentences = [
  'I like this place/object because it makes me feel ___.',
  'It always makes me happy when I see/touch/smell it.',
  'This place is special to me because ___.',
  'It helps me relax whenever I’m there.',
  'I enjoy spending time here more than anywhere else.',
  'It reminds me of ___, which is why I love it.',
  'I feel calm and peaceful when I am near it.',
  'It brings back memories of ___.',
  'I often go there when I want to ___.',
];

function showTopicSentence() {
  showRandomTemplate(topicSentences, 'Topic Sentence');
}
function showSensoryDetails() {
  showRandomTemplate(sensoryDetails, 'Sensory Details');
}
function showSpatialDetails() {
  showRandomTemplate(spatialDetails, 'Spatial / Additional Details');
}
function showConcludingSentence() {
  showRandomTemplate(concludingSentences, 'Concluding Sentence');
}
function showRandomTemplate(list, label) {
  // Past tense converterのoutputには一切触れず、templateOutputのみを使う
  const templateOutput = document.getElementById('templateOutput');
  const idx = Math.floor(Math.random() * list.length);
  templateOutput.innerText = `${label}:\n${list[idx]}`;
}
