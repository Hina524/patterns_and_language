#!/usr/bin/env python3
from pattern_finder import PatternFinder

def test_case_7():
    """Test the gerund subject case"""
    print("=== TEST CASE 7: Gerund subjects ===")
    text1 = "Running quickly exhausted him completely."
    text2 = "Swimming slowly relaxed her totally."
    
    finder = PatternFinder(level=3)
    result = finder.analyze_texts([text1, text2])
    
    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"Found {len(result['patterns'])} patterns:")
    
    for pattern in result['patterns']:
        print(f"  - \"{pattern['pattern']}\" ({pattern['length']} tokens, {pattern['count']} occurrences)")
    
    return len(result['patterns']) > 0

def test_case_8():
    """Test the linking verb case"""
    print("\n=== TEST CASE 8: Linking verbs ===")
    text1 = "She seems very happy today."
    text2 = "He looks quite tired now."
    
    finder = PatternFinder(level=3)
    result = finder.analyze_texts([text1, text2])
    
    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"Found {len(result['patterns'])} patterns:")
    
    for pattern in result['patterns']:
        print(f"  - \"{pattern['pattern']}\" ({pattern['length']} tokens, {pattern['count']} occurrences)")
    
    return len(result['patterns']) > 0

def main():
    print("Testing the two previously failed test cases...")
    
    case7_passed = test_case_7()
    case8_passed = test_case_8()
    
    print(f"\n=== RESULTS ===")
    print(f"Test case 7 (Gerund subjects): {'✅ PASSED' if case7_passed else '❌ FAILED'}")
    print(f"Test case 8 (Linking verbs): {'✅ PASSED' if case8_passed else '❌ FAILED'}")
    
    if case7_passed and case8_passed:
        print("🎉 Both previously failed tests now pass!")
    else:
        print("❗ Some tests still failing")

if __name__ == '__main__':
    main()