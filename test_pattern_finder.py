#!/usr/bin/env python3

from pattern_finder import PatternFinder

def test_level3_phrase_analysis():
    """Test Level 3 phrase type analysis"""
    
    # Initialize pattern finder for level 3
    finder = PatternFinder(level=3)
    
    # Test texts
    texts = [
        "I like to read books in the library.",
        "She likes to study books at the library."
    ]
    
    print("=== Level 3 Phrase Analysis Test ===\n")
    
    # Analyze each text individually to see tokenization
    for i, text in enumerate(texts, 1):
        print(f"Text {i}: \"{text}\"")
        tokens = finder.tokenize(text)
        print("Tokenization:")
        for token, phrase_type in tokens:
            print(f"  {token}[{phrase_type}]")
        print()
    
    # Test pattern finding
    print("=== Pattern Finding Results ===")
    result = finder.analyze_texts(texts)
    
    if result.get('error'):
        print(f"Error: {result['error']}")
    else:
        print(f"Found {len(result['patterns'])} common patterns:\n")
        for i, pattern in enumerate(result['patterns'], 1):
            print(f"{i}. Pattern: \"{pattern['pattern']}\"")
            print(f"   Length: {pattern['length']} {'token' if pattern['length'] == 1 else 'tokens'}")
            print(f"   Total occurrences: {pattern['count']}")
            print(f"   Found in {pattern['texts']} file(s)")
            print()

if __name__ == '__main__':
    test_level3_phrase_analysis() 