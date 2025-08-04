#!/usr/bin/env python3
"""
Debug why patterns aren't being found even with correct tokenization
"""

from pattern_finder_enhanced import PatternFinder

# Test case 7
texts = [
    "Running quickly exhausted him completely.",
    "Swimming slowly relaxed her totally."
]

finder = PatternFinder(level=3)

# Tokenize both texts
token_sequences = []
for i, text in enumerate(texts):
    tokens = finder.tokenize(text)
    token_sequences.append((f"Text {i+1}", tokens))
    print(f"Text {i+1}: {tokens}")

print("\nLooking for patterns manually:")

# Check what patterns should exist
seq1 = token_sequences[0][1]
seq2 = token_sequences[1][1]

print(f"\nSequence 1 length: {len(seq1)}")
print(f"Sequence 2 length: {len(seq2)}")

# Check for single token matches
print("\nSingle token matches:")
for i, (token1, phrase1) in enumerate(seq1):
    for j, (token2, phrase2) in enumerate(seq2):
        if phrase1 == phrase2:
            print(f"  Position {i} in text1 matches position {j} in text2: [{phrase1}]")

# Check for 2-token patterns
print("\n2-token patterns:")
for i in range(len(seq1) - 1):
    pattern1 = (seq1[i], seq1[i+1])
    for j in range(len(seq2) - 1):
        pattern2 = (seq2[j], seq2[j+1])
        if pattern1[0][1] == pattern2[0][1] and pattern1[1][1] == pattern2[1][1]:
            print(f"  Pattern at {i}-{i+1} in text1 matches {j}-{j+1} in text2: [{pattern1[0][1]}] [{pattern1[1][1]}]")

# Run the actual pattern finder
print("\nRunning pattern finder:")
patterns = finder.find_common_patterns(token_sequences)
print(f"Found {len(patterns)} patterns")

if patterns:
    for pattern, count, num_files in patterns[:5]:
        print(f"  {finder.format_pattern(pattern)} (count: {count})")
else:
    # Debug the pattern finding logic
    print("\nDebugging find_common_patterns:")
    
    # Check base sequence
    base_idx = min(range(len(token_sequences)), key=lambda i: len(token_sequences[i][1]))
    base_file, base_seq = token_sequences[base_idx]
    print(f"Base sequence: {base_file}, length: {len(base_seq)}")
    
    # Try to find a simple pattern manually
    test_pattern = (('Running', 'VP'),)
    print(f"\nLooking for pattern {test_pattern}:")
    for file_path, seq in token_sequences:
        count = finder.count_pattern_in_sequence(test_pattern, seq)
        print(f"  In {file_path}: {count} occurrences")