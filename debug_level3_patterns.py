#!/usr/bin/env python3
"""
Debug script to analyze Level 3 pattern finding for failed test cases.
This script shows exactly what tokens and phrase types are generated
and traces through the pattern matching algorithm step by step.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pattern_finder import PatternFinder
import json

def debug_tokenization(finder, text, label):
    """Show detailed tokenization results for a text"""
    print(f"\n{'='*60}")
    print(f"Tokenizing {label}: \"{text}\"")
    print(f"{'='*60}")
    
    # Get spaCy doc for detailed analysis
    doc = finder.nlp(text)
    
    # Show raw spaCy analysis first
    print("\nRaw spaCy analysis:")
    print(f"{'Token':<15} {'POS':<10} {'Tag':<10} {'Dep':<10} {'Head':<15}")
    print("-" * 70)
    for token in doc:
        head_text = token.head.text if token.head != token else "ROOT"
        print(f"{token.text:<15} {token.pos_:<10} {token.tag_:<10} {token.dep_:<10} {head_text:<15}")
    
    # Show noun chunks
    print("\nNoun chunks detected:")
    for chunk in doc.noun_chunks:
        print(f"  '{chunk.text}' (tokens {chunk.start}-{chunk.end})")
    
    # Get Level 3 tokenization
    tokens = finder.tokenize(text)
    
    print(f"\nLevel 3 tokenization result ({len(tokens)} tokens):")
    for i, (token_text, phrase_type) in enumerate(tokens):
        print(f"  {i}: '{token_text}' [{phrase_type}]")
    
    return tokens

def debug_pattern_matching(finder, sequences, test_name):
    """Debug the pattern matching algorithm step by step"""
    print(f"\n{'#'*80}")
    print(f"DEBUGGING PATTERN MATCHING FOR {test_name}")
    print(f"{'#'*80}")
    
    if len(sequences) < 2:
        print("ERROR: Need at least 2 sequences")
        return
    
    # Find shortest sequence (base)
    base_idx = min(range(len(sequences)), key=lambda i: len(sequences[i][1]))
    base_label, base_seq = sequences[base_idx]
    
    print(f"\nBase sequence: {base_label} ({len(base_seq)} tokens)")
    print("Base tokens:", [(t[0], t[1]) for t in base_seq])
    
    # Try to find patterns of different lengths
    patterns_found = []
    
    print("\nSearching for patterns...")
    
    # Start with full sequence and work down
    for length in range(len(base_seq), 0, -1):
        print(f"\n--- Checking patterns of length {length} ---")
        
        for start in range(len(base_seq) - length + 1):
            pattern = tuple(base_seq[start:start + length])
            pattern_str = " ".join([f"{t[0]}[{t[1]}]" for t in pattern])
            
            print(f"\nPattern: {pattern_str}")
            print(f"  Starting at position {start}")
            
            # Check in all sequences
            found_in = []
            for seq_label, seq in sequences:
                count = finder.count_pattern_in_sequence(pattern, seq)
                if count > 0:
                    found_in.append(seq_label)
                    print(f"  ✓ Found in {seq_label}: {count} time(s)")
                    
                    # Show where it was found
                    for i in range(len(seq) - length + 1):
                        if tuple(seq[i:i + length]) == pattern:
                            match_str = " ".join([f"{t[0]}[{t[1]}]" for t in seq[i:i + length]])
                            print(f"    - At position {i}: {match_str}")
                else:
                    print(f"  ✗ NOT found in {seq_label}")
                    
                    # Debug why not found - show what's at each position
                    if length <= 3:  # Only for short patterns to avoid too much output
                        print(f"    Checking each position in {seq_label}:")
                        for i in range(len(seq) - length + 1):
                            subseq = seq[i:i + length]
                            subseq_str = " ".join([f"{t[0]}[{t[1]}]" for t in subseq])
                            matches = [p == s for p, s in zip(pattern, subseq)]
                            if any(matches):  # Show partial matches
                                print(f"      Position {i}: {subseq_str}")
                                for j, (p, s, m) in enumerate(zip(pattern, subseq, matches)):
                                    if not m:
                                        print(f"        Token {j}: '{p[0]}[{p[1]}]' != '{s[0]}[{s[1]}]'")
            
            if len(found_in) >= 2:
                patterns_found.append((pattern, len(found_in)))
                print(f"  => Pattern found in {len(found_in)} sequences!")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: Found {len(patterns_found)} patterns")
    for pattern, count in patterns_found:
        pattern_str = " ".join([f"{t[0]}[{t[1]}]" for t in pattern])
        print(f"  - \"{pattern_str}\" (in {count} sequences)")

def main():
    # Initialize Level 3 finder
    finder = PatternFinder(level=3)
    
    # Test case 7
    print("\n" + "="*80)
    print("TEST CASE 7: Gerund subjects")
    print("="*80)
    
    text1 = "Running quickly exhausted him completely."
    text2 = "Swimming slowly relaxed her totally."
    
    tokens1 = debug_tokenization(finder, text1, "Sentence 1")
    tokens2 = debug_tokenization(finder, text2, "Sentence 2")
    
    sequences = [("Sentence 1", tokens1), ("Sentence 2", tokens2)]
    debug_pattern_matching(finder, sequences, "Test 7")
    
    # Test case 8
    print("\n\n" + "="*80)
    print("TEST CASE 8: Linking verbs with adverbs")
    print("="*80)
    
    text3 = "She seems very happy today."
    text4 = "He looks quite tired now."
    
    tokens3 = debug_tokenization(finder, text3, "Sentence 3")
    tokens4 = debug_tokenization(finder, text4, "Sentence 4")
    
    sequences2 = [("Sentence 3", tokens3), ("Sentence 4", tokens4)]
    debug_pattern_matching(finder, sequences2, "Test 8")
    
    # Additional analysis: Check if exact matching is the issue
    print("\n\n" + "="*80)
    print("ANALYSIS: Why are patterns not matching?")
    print("="*80)
    
    print("\nComparing token representations:")
    print("\nTest 7 comparison:")
    print(f"  Token 0: '{tokens1[0]}' vs '{tokens2[0]}' - Equal? {tokens1[0] == tokens2[0]}")
    print(f"  Token 1: '{tokens1[1]}' vs '{tokens2[1]}' - Equal? {tokens1[1] == tokens2[1]}")
    
    print("\nTest 8 comparison:")
    print(f"  Token 0: '{tokens3[0]}' vs '{tokens4[0]}' - Equal? {tokens3[0] == tokens4[0]}")
    print(f"  Token 1: '{tokens3[1]}' vs '{tokens4[1]}' - Equal? {tokens3[1] == tokens4[1]}")
    
    # Test the exact matching logic
    print("\n\nTesting pattern matching logic directly:")
    
    # Create a simple test pattern
    test_pattern = [("Running", "VP"), ("quickly", "ADVP")]
    test_sequence = [("Running", "VP"), ("quickly", "ADVP"), ("exhausted", "VP")]
    
    print(f"\nTest pattern: {test_pattern}")
    print(f"Test sequence: {test_sequence}")
    
    # Check if pattern matches at position 0
    match = True
    for i, p in enumerate(test_pattern):
        if i < len(test_sequence) and test_sequence[i] == p:
            print(f"  Position {i}: {p} == {test_sequence[i]} ✓")
        else:
            print(f"  Position {i}: {p} != {test_sequence[i]} ✗")
            match = False
    
    print(f"Pattern matches at position 0: {match}")

if __name__ == "__main__":
    main()