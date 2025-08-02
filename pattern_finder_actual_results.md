# Pattern Finder Level 1 Actual Test Results

## Test 1: Simple word repetition
- Input: 
  - Text 1: "The cat is sleeping."
  - Text 2: "The cat is eating."
- Found 6 patterns:
  - Pattern 1: "The cat is" (3 tokens, 2 occurrences)
  - Pattern 2: "The cat" (2 tokens, 2 occurrences)
  - Pattern 3: "cat is" (2 tokens, 2 occurrences)
  - Pattern 4-6: Single tokens "The", "cat", "is"

## Test 2: Greeting patterns
- Input:
  - Text 1: "Hello, how are you today?"
  - Text 2: "Hello, how are you feeling?"
  - Text 3: "Hi, how are you doing?"
- Found 10 patterns:
  - Pattern 1: "Hello, how are you" (4 tokens, 2 occurrences, found in 2 files)
  - Pattern 2: "how are you" (3 tokens, 3 occurrences, found in 3 files)
  - Pattern 3: "Hello, how are" (3 tokens, 2 occurrences, found in 2 files)
  - Additional patterns include shorter sequences

## Test 3: Action sequences
- Input:
  - Text 1: "I wake up, brush my teeth, and eat breakfast."
  - Text 2: "She wakes up, brushes her teeth, and eats breakfast."
- Found 5 patterns:
  - Pattern 1: "teeth, and" (2 tokens, 2 occurrences)
  - Pattern 2-5: Single tokens "up,", "teeth,", "and", "breakfast."