#!/usr/bin/env python3
from pattern_finder import PatternFinder

def debug_pattern_matching():
    """Debug why patterns are not being found"""
    print("=== Debugging Pattern Matching ===")
    
    # Test case 7
    text1 = "Running quickly exhausted him completely."
    text2 = "Swimming slowly relaxed her totally."
    
    finder = PatternFinder(level=3)
    
    # Get token sequences
    tokens1 = finder.tokenize(text1)
    tokens2 = finder.tokenize(text2)
    
    print(f"Text 1 tokens: {tokens1}")
    print(f"Text 2 tokens: {tokens2}")
    
    # Look for any shared phrase types
    phrase_types1 = [phrase for token, phrase in tokens1]
    phrase_types2 = [phrase for token, phrase in tokens2]
    
    print(f"Phrase types 1: {phrase_types1}")
    print(f"Phrase types 2: {phrase_types2}")
    
    # Find common phrase types
    common_types = set(phrase_types1) & set(phrase_types2)
    print(f"Common phrase types: {common_types}")
    
    # Check if there are any token+phrase matches
    common_token_phrase = set(tokens1) & set(tokens2)
    print(f"Common (token, phrase) pairs: {common_token_phrase}")
    
    # Manual pattern search
    print("\n=== Manual Pattern Analysis ===")
    print("Looking for patterns manually...")
    
    # Try to find all possible 1-token patterns
    patterns_found = []
    for i, (token1, phrase1) in enumerate(tokens1):
        for j, (token2, phrase2) in enumerate(tokens2):
            if (token1, phrase1) == (token2, phrase2):
                patterns_found.append((token1, phrase1))
    
    print(f"1-token patterns found: {patterns_found}")
    
    # Test case 8
    print(f"\n=== Test Case 8 ===")
    text3 = "She seems very happy today."
    text4 = "He looks quite tired now."
    
    tokens3 = finder.tokenize(text3)
    tokens4 = finder.tokenize(text4)
    
    print(f"Text 3 tokens: {tokens3}")
    print(f"Text 4 tokens: {tokens4}")
    
    common_token_phrase2 = set(tokens3) & set(tokens4)
    print(f"Common (token, phrase) pairs: {common_token_phrase2}")

if __name__ == '__main__':
    debug_pattern_matching()