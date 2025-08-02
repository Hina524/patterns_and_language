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

// テキストエリア自動リサイズ機能
function autoResize(textarea) {
    // 高さをリセットしてスクロール高さを取得
    textarea.style.height = 'auto';
    
    // 内容に合わせて高さを調整（最小3行、最大10行）
    const minHeight = 3 * 24; // 3行分の高さ（行の高さを24pxと仮定）
    const maxHeight = 10 * 24; // 10行分の高さ
    const scrollHeight = textarea.scrollHeight;
    
    if (scrollHeight < minHeight) {
        textarea.style.height = minHeight + 'px';
    } else if (scrollHeight > maxHeight) {
        textarea.style.height = maxHeight + 'px';
        textarea.style.overflowY = 'scroll';
    } else {
        textarea.style.height = scrollHeight + 'px';
        textarea.style.overflowY = 'hidden';
    }
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
        try {
            const content = e.target.result;
            
            // 内容の検証
            if (typeof content !== 'string') {
                throw new Error('File content is not text');
            }
            
            // BOM除去
            const cleanContent = content.replace(/^\uFEFF/, '');
            
            // 基本的なテキストクリーニング
            const trimmedContent = cleanContent.trim();
            
            if (trimmedContent.length === 0) {
                alert(`File "${file.name}" appears to be empty and will be skipped.`);
                return;
            }
            
            // ファイル情報を保存
            const fileInfo = {
                name: file.name,
                content: trimmedContent,
                size: file.size
            };
            
            uploadedFiles.push(fileInfo);
            updateFileList();
            
        } catch (error) {
            console.error('Error reading file:', error);
            alert(`Error reading file "${file.name}": ${error.message}`);
        }
    };
    
    reader.onerror = function() {
        alert(`Failed to read file "${file.name}". Please try again.`);
    };
    
    try {
        reader.readAsText(file, 'UTF-8');
    } catch (error) {
        alert(`Failed to process file "${file.name}": ${error.message}`);
    }
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
        const contentPreview = file.content; // 全テキストを表示
        
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

// Pattern Finder機能 - Python API版
async function findPatterns() {
    let level = parseInt(document.getElementById('levelSelect').value);
    let output = document.getElementById('patternOutput');
    let outputSection = document.getElementById('patternOutputSection');
    let loading = document.getElementById('patternLoading');

    let texts = [];

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
    
    try {
        // Python APIを呼び出し
        const response = await fetch('/api/find-patterns', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                texts: texts,
                level: level
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        if (result.error) {
            output.innerText = "Error: " + result.error;
        } else {
            // 成功した場合の結果表示
            displayApiPatternResults(result, output);
        }
        
    } catch (error) {
        output.innerText = "Error connecting to analysis service: " + error.message + 
                          "\nPlease ensure the server is running and spaCy is installed.";
    }
    
    loading.style.display = "none";
    outputSection.style.display = "block";
}

// API結果表示関数
function displayApiPatternResults(result, output) {
    let displayText = `Analysis completed using ${currentInputMethod === 'file' ? 'uploaded files' : 'manual input'}\n`;
    displayText += `Analyzed ${result.num_texts} text(s) | Level ${result.level} analysis\n\n`;
    
    if (result.patterns.length === 0) {
        displayText += "No common patterns found.";
        output.innerText = displayText;
        return;
    }
    
    displayText += `Found ${result.patterns.length} common patterns:\n\n`;
    
    // パターンを表示
    for (let i = 0; i < result.patterns.length; i++) {
        let pattern = result.patterns[i];
        displayText += `${i + 1}. Pattern: "${pattern.pattern}"\n`;
        displayText += `   Length: ${pattern.length} ${pattern.length === 1 ? 'token' : 'tokens'}\n`;
        displayText += `   Total occurrences: ${pattern.count}\n`;
        displayText += `   Found in ${pattern.texts} file(s)\n\n`;
    }
    
    if (result.total_patterns > result.patterns.length) {
        displayText += `... and ${result.total_patterns - result.patterns.length} more patterns\n`;
    }
    
    output.innerText = displayText;
}



async function convertToPast() {
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
    
    try {
        const response = await fetch('/api/analyze-grammar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.error) {
            output.innerText = "Error: " + result.error;
        } else {
            // 結果の表示
            displayGrammarAnalysisResult(result, output);
        }
        
    } catch (error) {
        output.innerText = "Error connecting to analysis service: " + error.message + 
                          "\nPlease ensure the server is running and spaCy is installed.";
    }
    
    loading.style.display = "none";
    outputSection.style.display = "block";
}

// 文法分析結果の表示
function displayGrammarAnalysisResult(result, output) {
    const prepsText = result.prepositional_phrases.length > 0 ? 
        result.prepositional_phrases.map(p => `・${p}`).join("\n") : "・(none)";
    
    output.innerText = `${result.past_tense}\nsentence type:\n・${result.sentence_type}\nprepositional phrases: \n${prepsText}`;
}

// 古いcompromise.jsベースの関数群は削除されました
// 新しいPython + spaCyベースのAPIを使用します

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

// ページロード時の初期化
document.addEventListener('DOMContentLoaded', function() {
    // 自動リサイズ対象のテキストエリアを初期化
    const autoResizeTextareas = document.querySelectorAll('textarea.auto-resize');
    autoResizeTextareas.forEach(function(textarea) {
        // 初期状態で自動リサイズを実行
        autoResize(textarea);
        
        // キーボード入力以外でのサイズ調整（ペーストなど）
        textarea.addEventListener('paste', function() {
            setTimeout(function() {
                autoResize(textarea);
            }, 0);
        });
    });
});