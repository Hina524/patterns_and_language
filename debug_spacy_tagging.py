#!/usr/bin/env python3
import spacy
from pattern_finder import PatternFinder

def debug_sentence_analysis(sentence):
    """Debug spaCy analysis for a single sentence"""
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    
    print(f"\nSentence: \"{sentence}\"")
    print("Token analysis:")
    for token in doc:
        print(f"  {token.text:12} | POS: {token.pos_:8} | TAG: {token.tag_:6} | DEP: {token.dep_:10} | HEAD: {token.head.text}")
    
    # Test with PatternFinder Level 3
    finder = PatternFinder(level=3)
    tokens = finder.tokenize(sentence)
    print(f"Level 3 tokens: {tokens}")
    
    return tokens

def main():
    print("=== Debugging spaCy Tagging Issues ===")
    
    # Test case 7 - Gerund subjects
    print("\n" + "="*50)
    print("TEST CASE 7: Gerund subjects")
    sentence1 = "Running quickly exhausted him completely."
    sentence2 = "Swimming slowly relaxed her totally."
    
    tokens1 = debug_sentence_analysis(sentence1)
    tokens2 = debug_sentence_analysis(sentence2)
    
    print(f"\nComparison:")
    print(f"Sentence 1: {tokens1}")
    print(f"Sentence 2: {tokens2}")
    
    # Test case 8 - Linking verbs
    print("\n" + "="*50)
    print("TEST CASE 8: Linking verbs")
    sentence3 = "She seems very happy today."
    sentence4 = "He looks quite tired now."
    
    tokens3 = debug_sentence_analysis(sentence3)
    tokens4 = debug_sentence_analysis(sentence4)
    
    print(f"\nComparison:")
    print(f"Sentence 3: {tokens3}")
    print(f"Sentence 4: {tokens4}")
    
    # Analyze what patterns should exist
    print("\n" + "="*50)
    print("PATTERN ANALYSIS")
    
    # Test case 7
    print("\nTest case 7 - Expected patterns:")
    print("- Both should have [ADVP] (quickly/slowly)")
    print("- Both should have [VP] (exhausted/relaxed)")  
    print("- Both should have [NP] (him/her)")
    print("- Both should have [ADVP] (completely/totally)")
    
    # Test case 8  
    print("\nTest case 8 - Expected patterns:")
    print("- Both should have [NP] (She/He)")
    print("- Both should have [VP] (seems/looks)")
    print("- Both should have [ADJP] (very/quite)")
    print("- Both should have [ADJP] (happy/tired)")
    print("- Both should have similar time expressions (today/now)")

if __name__ == '__main__':
    main()