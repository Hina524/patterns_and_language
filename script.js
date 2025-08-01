// タブ切り替え機能
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    // すべてのタブコンテンツを非表示にする
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }
    
    // すべてのタブボタンからactiveクラスを削除
    tablinks = document.getElementsByClassName("tab-button");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    
    // 選択されたタブを表示し、ボタンにactiveクラスを追加
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

// テキスト入力エリアの動的追加機能
let textInputCounter = 2;
let uploadedFiles = [];
let currentInputMethod = 'text';

// 入力方法選択機能
function selectInputMethod(method) {
    currentInputMethod = method;
    
    // ボタンのアクティブ状態を更新
    document.getElementById('textInputMethodBtn').classList.toggle('active', method === 'text');
    document.getElementById('fileInputMethodBtn').classList.toggle('active', method === 'file');
    
    // 対応するエリアを表示/非表示
    document.getElementById('textInputArea').style.display = method === 'text' ? 'block' : 'none';
    document.getElementById('fileInputArea').style.display = method === 'file' ? 'block' : 'none';
    
    // ファイルエリアが選択された場合、アップロードされたファイルをクリア
    if (method === 'text') {
        uploadedFiles = [];
        document.getElementById('fileList').innerHTML = '';
    }
}

// ファイルアップロード機能
function handleFileSelect(files) {
    const fileArray = Array.from(files);
    
    // .txtファイルのみフィルタリング
    const txtFiles = fileArray.filter(file => {
        const isValid = file.name.toLowerCase().endsWith('.txt');
        if (!isValid) {
            alert(`"${file.name}" is not a .txt file and will be skipped.`);
        }
        return isValid;
    });
    
    if (txtFiles.length === 0) {
        alert('No valid .txt files selected.');
        return;
    }
    
    // ファイルを読み込む
    txtFiles.forEach(file => readFile(file));
}

function readFile(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        
        // ファイル情報を保存
        const fileInfo = {
            name: file.name,
            content: content.trim(),
            size: file.size
        };
        
        uploadedFiles.push(fileInfo);
        updateFileList();
    };
    
    reader.readAsText(file, 'UTF-8');
}

function updateFileList() {
    const fileListContainer = document.getElementById('fileList');
    
    if (uploadedFiles.length === 0) {
        fileListContainer.innerHTML = '';
        return;
    }
    
    let html = '<h4 class="w3-text-orange">Uploaded Files:</h4>';
    uploadedFiles.forEach((file, index) => {
        const sizeKB = (file.size / 1024).toFixed(1);
        const contentPreview = file.content.length > 100 ? 
            file.content.substring(0, 100) + '...' : file.content;
        
        html += `
            <div class="file-item w3-card w3-margin-bottom w3-padding">
                <div class="file-header">
                    <span class="file-name w3-text-orange">${file.name}</span>
                    <span class="file-size w3-text-gray">(${sizeKB} KB)</span>
                    <button class="remove-file-btn w3-button w3-small w3-text-red" onclick="removeFile(${index})" title="Remove">
                        <i class="em em-x"></i>
                    </button>
                </div>
                <div class="file-preview w3-text-gray w3-small w3-margin-top">${contentPreview}</div>
            </div>
        `;
    });
    
    fileListContainer.innerHTML = html;
}

function removeFile(index) {
    uploadedFiles.splice(index, 1);
    updateFileList();
}

// ドラッグ&ドロップ機能
function initDragAndDrop() {
    const dropArea = document.getElementById('fileDropArea');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight(e) {
        dropArea.classList.add('highlight');
    }
    
    function unhighlight(e) {
        dropArea.classList.remove('highlight');
    }
    
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFileSelect(files);
    }
}

// ページロード時にドラッグ&ドロップを初期化
document.addEventListener('DOMContentLoaded', function() {
    initDragAndDrop();
    
    // Pattern Finderタブのときのみファイルアップロード機能を有効にする
    const patternTab = document.getElementById('patternTab');
    if (patternTab) {
        // 初期状態ではテキスト入力を選択
        selectInputMethod('text');
    }
});

function addTextInput() {
    textInputCounter++;
    const container = document.getElementById('textInputContainer');
    
    const newInputGroup = document.createElement('div');
    newInputGroup.className = 'text-input-group';
    newInputGroup.innerHTML = `
        <div class="text-input-header">
            <span class="text-label">Text ${textInputCounter}</span>
            <button class="remove-text-btn w3-button w3-small w3-text-red" onclick="removeTextInput(this)" title="削除">
                <i class="em em-x"></i>
            </button>
        </div>
        <textarea class="pattern-text-input w3-input w3-border w3-margin-bottom" rows="3" 
            placeholder="Enter text ${textInputCounter} here..."
            aria-label="Text input ${textInputCounter}"></textarea>
    `;
    
    container.appendChild(newInputGroup);
}

function removeTextInput(button) {
    const inputGroups = document.querySelectorAll('.text-input-group');
    
    // 最低1つは残す
    if (inputGroups.length <= 1) {
        return;
    }
    
    const inputGroup = button.closest('.text-input-group');
    inputGroup.remove();
    
    // ラベルを更新
    updateTextLabels();
}

function updateTextLabels() {
    const inputGroups = document.querySelectorAll('.text-input-group');
    inputGroups.forEach((group, index) => {
        const label = group.querySelector('.text-label');
        label.textContent = `Text ${index + 1}`;
        
        const textarea = group.querySelector('textarea');
        textarea.setAttribute('aria-label', `Text input ${index + 1}`);
        textarea.setAttribute('placeholder', `Enter text ${index + 1} here...`);
    });
}

// Pattern Finder機能
function findPatterns() {
    let level = parseInt(document.getElementById('levelSelect').value);
    let output = document.getElementById('patternOutput');
    let outputSection = document.getElementById('patternOutputSection');
    let loading = document.getElementById('patternLoading');

    let texts = [];
    let fileContents = '';

    if (currentInputMethod === 'text') {
        // 全てのテキストエリアから値を取得
        const textareas = document.querySelectorAll('.pattern-text-input');
        texts = Array.from(textareas)
            .map(textarea => textarea.value.trim())
            .filter(text => text.length > 0);
    } else if (currentInputMethod === 'file') {
        // アップロードされたファイルからテキストを取得
        if (uploadedFiles.length === 0) {
            output.innerText = "Please upload at least one .txt file to analyze.";
            outputSection.style.display = "block";
            return;
        }
        
        texts = uploadedFiles.map(file => file.content).filter(content => content.length > 0);
        
        // ファイル内容を表示用に準備
        fileContents = '\n--- Uploaded File Contents ---\n\n';
        uploadedFiles.forEach((file, index) => {
            fileContents += `File ${index + 1}: ${file.name}\n`;
            fileContents += `Content: ${file.content}\n\n`;
        });
    }

    if (texts.length === 0) {
        output.innerText = "Please provide at least one text to analyze.";
        outputSection.style.display = "block";
        return;
    }
    
    if (texts.length < 2) {
        output.innerText = "Please provide at least 2 texts to find common patterns.";
        outputSection.style.display = "block";
        return;
    }

    loading.style.display = "inline-block";
    outputSection.style.display = "none";
    
    setTimeout(() => {
        try {
            // 各テキストをトークン化
            let tokenSequences = [];
            for (let i = 0; i < texts.length; i++) {
                let tokens = tokenizeText(texts[i], level);
                if (tokens && tokens.length > 0) {
                    tokenSequences.push({
                        index: i + 1,
                        tokens: tokens
                    });
                }
            }

            if (tokenSequences.length < 2) {
                output.innerText = "Need at least 2 valid texts to find patterns.";
                loading.style.display = "none";
                outputSection.style.display = "block";
                return;
            }

            // 共通パターンを検索
            let patterns = findCommonPatterns(tokenSequences, level);
            
            // 結果を表示
            displayPatternResults(patterns, tokenSequences.length, level, output, fileContents);
            
        } catch (error) {
            output.innerText = "Error processing texts: " + error.message;
        }
        
        loading.style.display = "none";
        outputSection.style.display = "block";
    }, 500);
}

function tokenizeText(text, level) {
    let doc = nlp(text);
    let tokens = [];
    
    doc.terms().forEach(term => {
        let token = term.text();
        if (token.trim()) {
            switch(level) {
                case 1:
                    // Simple tokens
                    tokens.push(token);
                    break;
                case 2:
                    // Token + POS
                    let pos = term.tags().join('|') || 'O';
                    tokens.push([token, pos]);
                    break;
                case 3:
                    // Token + phrase type
                    let phraseType = getPhraseType(term);
                    tokens.push([token, phraseType]);
                    break;
                case 4:
                    // Token + POS + phrase type
                    let pos4 = term.tags().join('|') || 'O';
                    let phraseType4 = getPhraseType(term);
                    tokens.push([token, pos4, phraseType4]);
                    break;
            }
        }
    });
    
    return tokens;
}

function getPhraseType(term) {
    // Simple phrase type detection
    if (term.has('#Noun')) return 'NP';
    if (term.has('#Verb')) return 'VP';
    if (term.has('#Preposition')) return 'PP';
    if (term.has('#Adjective')) return 'ADJP';
    if (term.has('#Adverb')) return 'ADVP';
    return 'O';
}

function findCommonPatterns(tokenSequences, level) {
    let patterns = new Map();
    
    // 最短のシーケンスを基準にする
    let baseSeq = tokenSequences.reduce((shortest, current) => 
        current.tokens.length < shortest.tokens.length ? current : shortest
    );
    
    // すべての可能な部分列をチェック
    for (let length = Math.min(baseSeq.tokens.length, 10); length > 0; length--) {
        for (let start = 0; start <= baseSeq.tokens.length - length; start++) {
            let pattern = baseSeq.tokens.slice(start, start + length);
            let patternKey = JSON.stringify(pattern);
            
            // このパターンが他のシーケンスにも存在するかチェック
            let foundInTexts = new Set();
            let totalCount = 0;
            
            for (let seq of tokenSequences) {
                let count = countPatternInSequence(pattern, seq.tokens, level);
                if (count > 0) {
                    foundInTexts.add(seq.index);
                    totalCount += count;
                }
            }
            
            // 少なくとも2つのテキストに存在する場合のみ保存
            if (foundInTexts.size >= 2) {
                if (!patterns.has(patternKey) || patterns.get(patternKey).count < totalCount) {
                    patterns.set(patternKey, {
                        pattern: pattern,
                        count: totalCount,
                        texts: foundInTexts.size,
                        length: length
                    });
                }
            }
        }
    }
    
    // 結果をソート（長さ、出現回数、テキスト数順）
    return Array.from(patterns.values()).sort((a, b) => {
        if (a.length !== b.length) return b.length - a.length;
        if (a.count !== b.count) return b.count - a.count;
        return b.texts - a.texts;
    });
}

function countPatternInSequence(pattern, sequence, level) {
    let count = 0;
    let patternLen = pattern.length;
    let seqLen = sequence.length;
    
    for (let i = 0; i <= seqLen - patternLen; i++) {
        let match = true;
        for (let j = 0; j < patternLen; j++) {
            if (!tokensEqual(pattern[j], sequence[i + j], level)) {
                match = false;
                break;
            }
        }
        if (match) {
            count++;
        }
    }
    
    return count;
}

function tokensEqual(token1, token2, level) {
    if (level === 1) {
        return token1 === token2;
    } else {
        return JSON.stringify(token1) === JSON.stringify(token2);
    }
}

function formatPattern(pattern, level) {
    switch(level) {
        case 1:
            return pattern.join(' ');
        case 2:
            return pattern.map(([token, pos]) => `${token}(${pos})`).join(' ');
        case 3:
            return pattern.map(([token, phrase]) => `${token}[${phrase}]`).join(' ');
        case 4:
            return pattern.map(([token, pos, phrase]) => `${token}(${pos})[${phrase}]`).join(' ');
    }
}

function displayPatternResults(patterns, numTexts, level, output, fileContents = '') {
    let result = `Analysis completed using ${currentInputMethod === 'file' ? 'uploaded files' : 'manual input'}\n`;
    result += `Analyzed ${numTexts} text(s) | Level ${level} analysis\n\n`;
    
    if (patterns.length === 0) {
        result += "No common patterns found.";
        if (fileContents) {
            result += fileContents;
        }
        output.innerText = result;
        return;
    }
    
    result += `Found ${patterns.length} common patterns:\n\n`;
    
    // 上位20個まで表示
    let maxDisplay = Math.min(20, patterns.length);
    for (let i = 0; i < maxDisplay; i++) {
        let p = patterns[i];
        let formatted = formatPattern(p.pattern, level);
        result += `${i + 1}. Pattern: "${formatted}"\n`;
        result += `   Length: ${p.length} tokens\n`;
        result += `   Total occurrences: ${p.count}\n`;
        result += `   Found in ${p.texts} text(s)\n\n`;
    }
    
    if (patterns.length > maxDisplay) {
        result += `... and ${patterns.length - maxDisplay} more patterns\n`;
    }
    
    // ファイルの内容を表示（ファイルアップロードの場合）
    if (fileContents) {
        result += fileContents;
    }
    
    output.innerText = result;
}

function convertToPast() {
    let text = document.getElementById('textInput').value;
    let output = document.getElementById('output');
    let outputSection = document.getElementById('outputSection');
    let loading = document.getElementById('loading');

    if (text.trim() === "") {
        output.innerText = "Please enter some text.";
        outputSection.style.display = "block";
        return;
    }

    loading.style.display = "inline-block";
    outputSection.style.display = "none";
    
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
        outputSection.style.display = "block";
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
    let matches = doc.match('#Preposition .+? #Noun');
    matches.forEach(m => {
        preps.push(m.text());
    });
    return preps;
}

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
    const templateOutputSection = document.getElementById('templateOutputSection');
    const idx = Math.floor(Math.random() * list.length);
    templateOutput.innerText = `${label}:\n${list[idx]}`;
    templateOutputSection.style.display = "block";
}