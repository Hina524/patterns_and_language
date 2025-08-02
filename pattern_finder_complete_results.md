# Pattern Finder Level 1 Complete Test Results

## Test 1: Simple word repetition ✅
- Input: 
  - Text 1: "The cat is sleeping."
  - Text 2: "The cat is eating."
- Results: Found 6 common patterns
  - "The cat is" (3 tokens, 2 occurrences)
  - "The cat" (2 tokens, 2 occurrences)
  - "cat is" (2 tokens, 2 occurrences)
  - "The" (1 token, 2 occurrences)
  - "cat" (1 token, 2 occurrences)
  - "is" (1 token, 2 occurrences)

## Test 2: Greeting patterns ✅
- Input:
  - Text 1: "Hello, how are you today?"
  - Text 2: "Hello, how are you feeling?"
  - Text 3: "Hi, how are you doing?"
- Results: Found 10 common patterns
  - "Hello, how are you" (4 tokens, 2 occurrences, 2 files)
  - "how are you" (3 tokens, 3 occurrences, 3 files)
  - "Hello, how are" (3 tokens, 2 occurrences, 2 files)
  - Additional shorter patterns

## Test 3: Action sequences ✅
- Input:
  - Text 1: "I wake up, brush my teeth, and eat breakfast."
  - Text 2: "She wakes up, brushes her teeth, and eats breakfast."
- Results: Found 5 common patterns
  - "teeth, and" (2 tokens, 2 occurrences)
  - "up," (1 token, 2 occurrences)
  - "teeth," (1 token, 2 occurrences)
  - "and" (1 token, 2 occurrences)
  - "breakfast." (1 token, 2 occurrences)

## Test 4: Question structures ✅
- Input:
  - Text 1: "What is your favorite color?"
  - Text 2: "What is your favorite food?"
  - Text 3: "What is your favorite movie?"
- Results: Found 10 common patterns
  - "What is your favorite" (4 tokens, 3 occurrences, 3 files)
  - "What is your" (3 tokens, 3 occurrences, 3 files)
  - "is your favorite" (3 tokens, 3 occurrences, 3 files)
  - Additional shorter patterns all found in 3 files