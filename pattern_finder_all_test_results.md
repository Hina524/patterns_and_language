# Pattern Finder Level 1 - All Test Results (Actual)

## Test 1: Simple word repetition ✅
- Input: 
  - Text 1: "The cat is sleeping."
  - Text 2: "The cat is eating."
- **Actual Results**: Found 6 common patterns
  - "The cat is" (3 tokens, 2 occurrences)
  - "The cat" (2 tokens, 2 occurrences)
  - "cat is" (2 tokens, 2 occurrences)
  - Single tokens: "The", "cat", "is"

## Test 2: Greeting patterns ✅
- Input:
  - Text 1: "Hello, how are you today?"
  - Text 2: "Hello, how are you feeling?"
  - Text 3: "Hi, how are you doing?"
- **Actual Results**: Found 10 common patterns
  - "Hello, how are you" (4 tokens, 2 files)
  - "how are you" (3 tokens, 3 files)
  - "Hello, how are" (3 tokens, 2 files)
  - Additional patterns include shorter sequences

## Test 3: Action sequences ✅
- Input:
  - Text 1: "I wake up, brush my teeth, and eat breakfast."
  - Text 2: "She wakes up, brushes her teeth, and eats breakfast."
- **Actual Results**: Found 5 common patterns
  - "teeth, and" (2 tokens, 2 occurrences)
  - Single tokens: "up,", "teeth,", "and", "breakfast."

## Test 4: Question structures ✅
- Input:
  - Text 1: "What is your favorite color?"
  - Text 2: "What is your favorite food?"
  - Text 3: "What is your favorite movie?"
- **Actual Results**: Found 10 common patterns
  - "What is your favorite" (4 tokens, 3 files)
  - "What is your" (3 tokens, 3 files)
  - "is your favorite" (3 tokens, 3 files)
  - All patterns found in all 3 files

## Test 5: Time expressions ✅
- Input:
  - Text 1: "Every morning I go for a walk."
  - Text 2: "Every morning she goes for a run."
  - Text 3: "Every morning they go for a swim."
- **Actual Results**: Found 9 common patterns
  - "go for a" (3 tokens, 2 files)
  - "Every morning" (2 tokens, 3 files)
  - "for a" (2 tokens, 3 files)
  - "go for" (2 tokens, 2 files)

## Test 6: Conditional patterns ✅
- Input:
  - Text 1: "If it rains, I will stay home."
  - Text 2: "If it snows, I will stay inside."
- **Actual Results**: Found 9 common patterns
  - "I will stay" (3 tokens, 2 occurrences)
  - "If it" (2 tokens, 2 occurrences)
  - "I will" (2 tokens, 2 occurrences)
  - "will stay" (2 tokens, 2 occurrences)
  - Single tokens: "If", "it", "I", "will", "stay"

## Test 7: Comparative structures ✅
- Input:
  - Text 1: "This book is better than that one."
  - Text 2: "This movie is better than that one."
- **Actual Results**: Found 16 common patterns
  - "is better than that one." (5 tokens, 2 occurrences)
  - Multiple 4-token patterns
  - Multiple 3-token patterns
  - All single tokens matched