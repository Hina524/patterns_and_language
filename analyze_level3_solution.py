#!/usr/bin/env python3
"""
Analysis script to understand Level 3 pattern matching behavior
and explore potential solutions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pattern_finder import PatternFinder
import spacy

def test_abstract_patterns():
    """Test if we can find patterns by looking at phrase types only"""
    
    print("="*80)
    print("TESTING ABSTRACT PATTERN MATCHING (phrase types only)")
    print("="*80)
    
    finder = PatternFinder(level=3)
    
    # Test case 7
    text1 = "Running quickly exhausted him completely."
    text2 = "Swimming slowly relaxed her totally."
    
    tokens1 = finder.tokenize(text1)
    tokens2 = finder.tokenize(text2)
    
    print("\nTest 7 - Phrase type sequences:")
    phrase_seq1 = [phrase for _, phrase in tokens1]
    phrase_seq2 = [phrase for _, phrase in tokens2]
    
    print(f"Sentence 1: {phrase_seq1}")
    print(f"Sentence 2: {phrase_seq2}")
    
    # Find common phrase patterns
    print("\nLooking for common phrase patterns:")
    for length in range(min(len(phrase_seq1), len(phrase_seq2)), 0, -1):
        for start1 in range(len(phrase_seq1) - length + 1):
            pattern = phrase_seq1[start1:start1 + length]
            
            # Check if this pattern exists in sequence 2
            for start2 in range(len(phrase_seq2) - length + 1):
                if phrase_seq2[start2:start2 + length] == pattern:
                    print(f"  Found common phrase pattern: {pattern}")
                    print(f"    In sentence 1 at position {start1}: {[tokens1[i][0] for i in range(start1, start1+length)]}")
                    print(f"    In sentence 2 at position {start2}: {[tokens2[i][0] for i in range(start2, start2+length)]}")
    
    # Test case 8
    text3 = "She seems very happy today."
    text4 = "He looks quite tired now."
    
    tokens3 = finder.tokenize(text3)
    tokens4 = finder.tokenize(text4)
    
    print("\n\nTest 8 - Phrase type sequences:")
    phrase_seq3 = [phrase for _, phrase in tokens3]
    phrase_seq4 = [phrase for _, phrase in tokens4]
    
    print(f"Sentence 3: {phrase_seq3}")
    print(f"Sentence 4: {phrase_seq4}")
    
    print("\nLooking for common phrase patterns:")
    for length in range(min(len(phrase_seq3), len(phrase_seq4)), 0, -1):
        for start1 in range(len(phrase_seq3) - length + 1):
            pattern = phrase_seq3[start1:start1 + length]
            
            # Check if this pattern exists in sequence 4
            for start2 in range(len(phrase_seq4) - length + 1):
                if phrase_seq4[start2:start2 + length] == pattern:
                    print(f"  Found common phrase pattern: {pattern}")
                    print(f"    In sentence 3 at position {start1}: {[tokens3[i][0] for i in range(start1, start1+length)]}")
                    print(f"    In sentence 4 at position {start2}: {[tokens4[i][0] for i in range(start2, start2+length)]}")
                    break

def analyze_spacy_tagging():
    """Analyze why spaCy tags gerunds differently"""
    
    print("\n\n" + "="*80)
    print("ANALYZING SPACY TAGGING INCONSISTENCY")
    print("="*80)
    
    nlp = spacy.load('en_core_web_sm')
    
    # Test different gerund sentences
    test_sentences = [
        "Running quickly exhausted him completely.",
        "Swimming slowly relaxed her totally.",
        "Walking fast tired me out.",
        "Reading carefully helped her understand.",
        "Singing loudly annoyed the neighbors."
    ]
    
    print("\nAnalyzing gerund tagging patterns:")
    for sent in test_sentences:
        doc = nlp(sent)
        first_token = doc[0]
        print(f"\n'{sent}'")
        print(f"  First word: '{first_token.text}'")
        print(f"  POS: {first_token.pos_}, TAG: {first_token.tag_}, DEP: {first_token.dep_}")
        
        # Check if it's in a noun chunk
        in_noun_chunk = any(first_token.i >= chunk.start and first_token.i < chunk.end 
                           for chunk in doc.noun_chunks)
        print(f"  In noun chunk: {in_noun_chunk}")

def propose_solution():
    """Propose a solution for Level 3 pattern matching"""
    
    print("\n\n" + "="*80)
    print("PROPOSED SOLUTIONS")
    print("="*80)
    
    print("\nOption 1: Modify Level 3 to match on phrase types only")
    print("  - Change pattern matching to ignore token text for Level 3")
    print("  - Would find patterns like [NP] [VP] [ADJP] [ADJP]")
    print("  - This would match the expected behavior for grammatical pattern finding")
    
    print("\nOption 2: Add special handling for gerunds")
    print("  - Detect gerunds (-ing verbs) used as subjects")
    print("  - Classify them consistently as VP or NP")
    print("  - Would fix Test 7 but not Test 8")
    
    print("\nOption 3: Create a new level for abstract patterns")
    print("  - Level 3: token + phrase (current behavior)")
    print("  - Level 5: phrase patterns only (new)")
    print("  - Allows both concrete and abstract pattern matching")
    
    print("\nOption 4: Hybrid approach")
    print("  - For Level 3, find patterns that match on phrase type")
    print("  - But display them with example tokens from the first occurrence")
    print("  - E.g., 'She[NP] seems[VP] very[ADJP] happy[ADJP]' would match")
    print("         'He[NP] looks[VP] quite[ADJP] tired[ADJP]'")

def test_modified_matching():
    """Test what would happen with phrase-only matching"""
    
    print("\n\n" + "="*80)
    print("SIMULATING PHRASE-ONLY MATCHING")
    print("="*80)
    
    finder = PatternFinder(level=3)
    
    test_cases = [
        ("Test 7", [
            "Running quickly exhausted him completely.",
            "Swimming slowly relaxed her totally."
        ]),
        ("Test 8", [
            "She seems very happy today.",
            "He looks quite tired now."
        ])
    ]
    
    for test_name, sentences in test_cases:
        print(f"\n{test_name}:")
        
        # Get tokens and create phrase-only sequences
        all_tokens = []
        phrase_sequences = []
        
        for i, sent in enumerate(sentences):
            tokens = finder.tokenize(sent)
            all_tokens.append(tokens)
            phrase_seq = [phrase for _, phrase in tokens]
            phrase_sequences.append((f"Sentence {i+1}", phrase_seq))
            
            print(f"  Sentence {i+1}: {sent}")
            print(f"    Tokens: {[f'{t}[{p}]' for t, p in tokens]}")
            print(f"    Phrases: {phrase_seq}")
        
        # Find common phrase patterns (simulating phrase-only matching)
        print(f"\n  Common phrase patterns found:")
        
        if len(phrase_sequences) >= 2:
            seq1_phrases = phrase_sequences[0][1]
            seq2_phrases = phrase_sequences[1][1]
            
            patterns_found = []
            
            for length in range(min(len(seq1_phrases), len(seq2_phrases)), 0, -1):
                for start1 in range(len(seq1_phrases) - length + 1):
                    pattern = seq1_phrases[start1:start1 + length]
                    
                    for start2 in range(len(seq2_phrases) - length + 1):
                        if seq2_phrases[start2:start2 + length] == pattern:
                            # Get example tokens from first sentence
                            example_tokens = all_tokens[0][start1:start1 + length]
                            example_str = " ".join([f"{t}[{p}]" for t, p in example_tokens])
                            
                            if pattern not in [p[0] for p in patterns_found]:
                                patterns_found.append((pattern, example_str, length))
            
            # Sort by length (longest first)
            patterns_found.sort(key=lambda x: x[2], reverse=True)
            
            for pattern, example, length in patterns_found:
                print(f"    - Pattern: {pattern} (length {length})")
                print(f"      Example: \"{example}\"")

if __name__ == "__main__":
    test_abstract_patterns()
    analyze_spacy_tagging()
    propose_solution()
    test_modified_matching()