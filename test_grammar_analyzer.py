#!/usr/bin/env python3
"""
Test script for the new English Grammar Analyzer
Tests the specific problem cases from grammar_analyzer_test_results.md
"""

from english_grammar_analyzer import EnglishGrammarAnalyzer


def test_problem_cases():
    """
    Test cases that had issues in the original implementation
    """
    analyzer = EnglishGrammarAnalyzer()
    
    # Test cases with expected improvements
    test_cases = [
        {
            "id": 2,
            "input": "She writes beautiful poems in her notebook.",
            "expected_issues": ["Prepositional phrase incomplete: 'in her' instead of 'in her notebook'"],
        },
        {
            "id": 3, 
            "input": "Students study hard before the exam.",
            "expected_issues": ["'before the exam' is a prepositional phrase, not detected"],
        },
        {
            "id": 7,
            "input": "We can go to the park, or we can stay home.",
            "expected_issues": ["'to the park' is a prepositional phrase, not detected"],
        },
        {
            "id": 12,
            "input": "I go to school, eat lunch, and come back home.",
            "expected_issues": ["'to school' is a prepositional phrase, not detected"],
        },
        {
            "id": 14,
            "input": "They swim in the pool, run in the park, and fly kites.",
            "expected_issues": ["Only first verb converted to past tense"],
        },
        {
            "id": 15,
            "input": "The book on the table in the library belongs to the student from Japan.",
            "expected_issues": ["'to the student' prepositional phrase missing"],
        },
        {
            "id": 16,
            "input": "During the summer, children play in the garden behind the house near the river.",
            "expected_issues": ["Missing 'behind the house' and 'near the river'"],
        },
        {
            "id": 18,
            "input": "When the sun rises, birds sing because they feel happy, although some people still sleep.",
            "expected_issues": ["Inconsistent past tense conversion"],
        }
    ]
    
    print("🧪 Testing English Grammar Analyzer - Problem Cases")
    print("=" * 60)
    
    for test_case in test_cases:
        print(f"\n📝 Test Case #{test_case['id']}")
        print(f"Input: {test_case['input']}")
        print(f"Known Issues: {', '.join(test_case['expected_issues'])}")
        print("-" * 40)
        
        try:
            result = analyzer.analyze_text(test_case['input'])
            
            if result.get('error'):
                print(f"❌ Error: {result['error']}")
                continue
            
            print(f"✅ Past Tense: {result['past_tense']}")
            print(f"✅ Sentence Type: {result['sentence_type']}")
            print(f"✅ Prepositional Phrases: {', '.join(result['prepositional_phrases']) if result['prepositional_phrases'] else '(none)'}")
            
            # Basic validation
            print("\n🔍 Analysis:")
            
            # Check if past tense conversion looks improved
            past_verbs = count_past_tense_verbs(result['past_tense'])
            original_verbs = count_verbs_in_text(test_case['input'])
            if past_verbs >= original_verbs:
                print(f"   ✅ Verb conversion: {past_verbs} past tense verbs detected")
            else:
                print(f"   ⚠️  Verb conversion: Only {past_verbs}/{original_verbs} verbs converted")
            
            # Check prepositional phrase count
            prep_count = len(result['prepositional_phrases'])
            if prep_count > 0:
                print(f"   ✅ Prepositional phrases: {prep_count} detected")
                for i, phrase in enumerate(result['prepositional_phrases'], 1):
                    print(f"      {i}. '{phrase}'")
            else:
                print(f"   ℹ️  Prepositional phrases: None detected")
                
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
        
        print()


def count_past_tense_verbs(text):
    """Simple heuristic to count potential past tense verbs"""
    analyzer = EnglishGrammarAnalyzer()
    doc = analyzer.nlp(text)
    past_verbs = 0
    for token in doc:
        if token.pos_ in ['VERB', 'AUX'] and token.tag_ in ['VBD', 'VBN']:
            past_verbs += 1
    return past_verbs


def count_verbs_in_text(text):
    """Count total verbs in original text"""
    analyzer = EnglishGrammarAnalyzer()
    doc = analyzer.nlp(text)
    verb_count = 0
    for token in doc:
        if token.pos_ in ['VERB', 'AUX']:
            verb_count += 1
    return verb_count


def quick_functionality_test():
    """Quick test to ensure basic functionality works"""
    print("🚀 Quick Functionality Test")
    print("=" * 30)
    
    analyzer = EnglishGrammarAnalyzer()
    
    simple_tests = [
        "The cat sleeps on the mat.",
        "I like coffee, but she prefers tea.",
        "Although it rains, we continue our journey."
    ]
    
    for i, test in enumerate(simple_tests, 1):
        print(f"\n{i}. Input: {test}")
        result = analyzer.analyze_text(test)
        
        if result.get('error'):
            print(f"   ❌ Error: {result['error']}")
        else:
            print(f"   Past: {result['past_tense']}")
            print(f"   Type: {result['sentence_type']}")
            print(f"   Phrases: {result['prepositional_phrases']}")


if __name__ == "__main__":
    print("English Grammar Analyzer Test Suite")
    print("===================================\n")
    
    try:
        # Quick functionality test first
        quick_functionality_test()
        print("\n" + "="*60 + "\n")
        
        # Detailed problem case testing
        test_problem_cases()
        
        print("\n🎉 Testing Complete!")
        print("\nTo run the web application:")
        print("  python app.py")
        print("\nTo test individual cases:")
        print("  python english_grammar_analyzer.py")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        print("\nMake sure spaCy English model is installed:")
        print("  python -m spacy download en_core_web_sm") 