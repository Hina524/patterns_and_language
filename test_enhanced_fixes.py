#!/usr/bin/env python3
"""
Test the enhanced pattern finder with the failed test cases
"""

from pattern_finder_enhanced import PatternFinder

# Test cases that failed in the original
test_cases = [
    {
        "test_num": 7,
        "name": "Gerund VP as subject",
        "texts": [
            "Running quickly exhausted him completely.",
            "Swimming slowly relaxed her totally."
        ]
    },
    {
        "test_num": 8,
        "name": "Linking verb + ADJP pattern",
        "texts": [
            "She seems very happy today.",
            "He looks quite tired now."
        ]
    }
]

print("=" * 80)
print("Testing Enhanced Pattern Finder")
print("=" * 80)

# Create enhanced pattern finder
finder = PatternFinder(level=3)

for test in test_cases:
    print(f"\nTest #{test['test_num']}: {test['name']}")
    print("-" * 60)
    
    # Analyze texts
    result = finder.analyze_texts(test['texts'])
    
    if result.get('success'):
        print(f"Found {len(result['patterns'])} patterns:")
        for i, pattern in enumerate(result['patterns'], 1):
            print(f"{i}. \"{pattern['pattern']}\" ({pattern['length']} tokens, {pattern['count']} occurrences)")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Show tokenization details
    print("\nTokenization details:")
    for i, text in enumerate(test['texts'], 1):
        tokens = finder.tokenize(text)
        formatted = finder.format_pattern(tokens)
        print(f"Text {i}: {formatted}")

print("\n" + "=" * 80)
print("COMPARISON WITH EXPECTED RESULTS")
print("=" * 80)

print("\nTest 7 - Expected to find patterns like:")
print("- Gerund[VP] + adverb[ADVP] pattern")
print("- verb[VP] + pronoun[NP] + adverb[ADVP] pattern")

print("\nTest 8 - Expected to find patterns like:")
print("- pronoun[NP] + linking_verb[VP] pattern")
print("- intensifier[ADVP] + adjective[ADJP] pattern")
print("- time/place_adverb[ADVP] at end")