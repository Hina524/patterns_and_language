#!/usr/bin/env python3
import spacy
from pattern_finder import PatternFinder

# Initialize spaCy and pattern finder
nlp = spacy.load('en_core_web_sm')
finder = PatternFinder(level=3)

# Test 7: Gerund VP as subject
test7_texts = [
    "Running quickly exhausted him completely.",
    "Swimming slowly relaxed her totally."
]

# Test 8: Linking verb + ADJP pattern
test8_texts = [
    "She seems very happy today.",
    "He looks quite tired now."
]

def analyze_sentence(text, test_name):
    print(f"\n{'='*60}")
    print(f"{test_name}: {text}")
    print('='*60)
    
    # Parse with spaCy
    doc = nlp(text)
    
    # Show token details
    print("\nToken Analysis:")
    print(f"{'Token':<15} {'POS':<10} {'TAG':<10} {'DEP':<15} {'HEAD':<15}")
    print('-'*70)
    for token in doc:
        print(f"{token.text:<15} {token.pos_:<10} {token.tag_:<10} {token.dep_:<15} {token.head.text:<15}")
    
    # Show noun chunks
    print("\nNoun Chunks:")
    for chunk in doc.noun_chunks:
        print(f"  '{chunk.text}' (span: {chunk.start}-{chunk.end})")
    
    # Build phrase map using PatternFinder's method
    phrase_map = finder._build_phrase_map(doc)
    
    # Show phrase types assigned
    print("\nPhrase Type Assignment:")
    for i, token in enumerate(doc):
        if not token.is_space and token.pos_ != 'PUNCT':
            phrase_type = phrase_map.get(i, 'O')
            print(f"  {token.text} -> {phrase_type}")
    
    # Tokenize using PatternFinder
    tokens = finder.tokenize(text)
    print("\nPatternFinder Tokenization:")
    print(tokens)
    
    return tokens

# Analyze Test 7
print("\n" + "="*80)
print("TEST 7 ANALYSIS: Gerund VP as subject")
print("="*80)

test7_results = []
for text in test7_texts:
    tokens = analyze_sentence(text, "Test 7")
    test7_results.append(tokens)

# Find patterns for Test 7
print("\n" + "="*60)
print("Test 7 Pattern Finding:")
token_sequences = [(f"Text {i+1}", tokens) for i, tokens in enumerate(test7_results)]
patterns = finder.find_common_patterns(token_sequences)
if patterns:
    for pattern, count, num_files in patterns[:5]:
        formatted = finder.format_pattern(pattern)
        print(f"  Pattern: '{formatted}' (count: {count}, files: {num_files})")
else:
    print("  No patterns found!")

# Analyze Test 8
print("\n" + "="*80)
print("TEST 8 ANALYSIS: Linking verb + ADJP pattern")
print("="*80)

test8_results = []
for text in test8_texts:
    tokens = analyze_sentence(text, "Test 8")
    test8_results.append(tokens)

# Find patterns for Test 8
print("\n" + "="*60)
print("Test 8 Pattern Finding:")
token_sequences = [(f"Text {i+1}", tokens) for i, tokens in enumerate(test8_results)]
patterns = finder.find_common_patterns(token_sequences)
if patterns:
    for pattern, count, num_files in patterns[:5]:
        formatted = finder.format_pattern(pattern)
        print(f"  Pattern: '{formatted}' (count: {count}, files: {num_files})")
else:
    print("  No patterns found!")

# Additional debugging: Show what patterns we might expect
print("\n" + "="*80)
print("EXPECTED PATTERNS ANALYSIS")
print("="*80)

print("\nTest 7 - Expected patterns:")
print("  - Gerund (Running/Swimming) should be marked as VP or NP")
print("  - Adverb (quickly/slowly) should be ADVP")
print("  - Main verb (exhausted/relaxed) should be VP")
print("  - Object pronoun (him/her) should be NP")
print("  - Final adverb (completely/totally) should be ADVP")

print("\nTest 8 - Expected patterns:")
print("  - Subject pronoun (She/He) should be NP")
print("  - Linking verb (seems/looks) should be VP")
print("  - Degree adverb (very/quite) should be ADVP or part of ADJP")
print("  - Adjective (happy/tired) should be ADJP")
print("  - Time adverb (today/now) should be ADVP")

# Let's check if the issue is with the pattern matching logic
print("\n" + "="*80)
print("MANUAL PATTERN CHECK")
print("="*80)

# Manually check for potential patterns
def check_manual_patterns(tokens1, tokens2):
    print(f"\nTokens 1: {tokens1}")
    print(f"Tokens 2: {tokens2}")
    
    # Extract just the phrase types
    phrases1 = [phrase for _, phrase in tokens1]
    phrases2 = [phrase for _, phrase in tokens2]
    
    print(f"\nPhrase types 1: {phrases1}")
    print(f"Phrase types 2: {phrases2}")
    
    # Check for common phrase type sequences
    common_sequences = []
    for i in range(len(phrases1)):
        for j in range(i+1, len(phrases1)+1):
            seq1 = phrases1[i:j]
            # Check if this sequence exists in phrases2
            for k in range(len(phrases2) - len(seq1) + 1):
                if phrases2[k:k+len(seq1)] == seq1:
                    common_sequences.append(seq1)
    
    print(f"\nCommon phrase type sequences: {common_sequences}")

print("\nTest 7 manual pattern check:")
check_manual_patterns(test7_results[0], test7_results[1])

print("\nTest 8 manual pattern check:")
check_manual_patterns(test8_results[0], test8_results[1])