#!/usr/bin/env python3
"""
SpaCy Analysis Debug Script
Detailed analysis of how spaCy is tokenizing and tagging the failed test sentences
"""

import spacy
import json
from pattern_finder import PatternFinder

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Failed test cases
failed_tests = [
    {
        "test_num": 7,
        "texts": [
            "Running quickly exhausted him completely.",
            "Swimming slowly relaxed her totally."
        ],
        "expected_pattern": "Gerund VP as subject"
    },
    {
        "test_num": 8,
        "texts": [
            "She seems very happy today.",
            "He looks quite tired now."
        ],
        "expected_pattern": "Linking verb + ADJP pattern"
    }
]

def analyze_token_details(doc):
    """Analyze each token in detail"""
    tokens = []
    for token in doc:
        token_info = {
            "text": token.text,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "lemma": token.lemma_,
            "is_stop": token.is_stop,
            "head": token.head.text,
            "children": [child.text for child in token.children]
        }
        tokens.append(token_info)
    return tokens

def analyze_noun_chunks(doc):
    """Analyze noun chunks in the document"""
    chunks = []
    for chunk in doc.noun_chunks:
        chunks.append({
            "text": chunk.text,
            "root": chunk.root.text,
            "start": chunk.start,
            "end": chunk.end
        })
    return chunks

def analyze_phrase_detection(finder, text):
    """Analyze how the pattern finder builds phrases"""
    doc = nlp(text)
    phrase_map = finder._build_phrase_map(doc)
    
    phrase_assignments = []
    for token in doc:
        if not token.is_space:
            phrase_type = phrase_map.get(token.i, 'O')
            phrase_assignments.append({
                "token": token.text,
                "pos": token.pos_,
                "phrase_type": phrase_type
            })
    
    return phrase_assignments

print("=" * 80)
print("SpaCy Token Analysis Debug Report")
print("=" * 80)

# Create pattern finder instance
finder = PatternFinder(level=3)

for test in failed_tests:
    print(f"\nTest #{test['test_num']}: {test['expected_pattern']}")
    print("-" * 60)
    
    for i, text in enumerate(test['texts'], 1):
        print(f"\nText {i}: \"{text}\"")
        doc = nlp(text)
        
        # Basic token analysis
        print("\n1. Token Analysis:")
        tokens = analyze_token_details(doc)
        for j, token in enumerate(tokens):
            print(f"   [{j}] '{token['text']}': POS={token['pos']}, TAG={token['tag']}, "
                  f"DEP={token['dep']}, HEAD='{token['head']}'")
        
        # Noun chunks
        print("\n2. Noun Chunks:")
        chunks = analyze_noun_chunks(doc)
        if chunks:
            for chunk in chunks:
                print(f"   - '{chunk['text']}' (tokens {chunk['start']}-{chunk['end']})")
        else:
            print("   - No noun chunks detected")
        
        # Phrase detection
        print("\n3. Phrase Type Assignment:")
        phrase_assignments = analyze_phrase_detection(finder, text)
        for assignment in phrase_assignments:
            print(f"   - '{assignment['token']}' ({assignment['pos']}) -> {assignment['phrase_type']}")
        
        # Final tokenization result
        print("\n4. Final Level 3 Tokenization:")
        level3_tokens = finder.tokenize(text)
        formatted = finder.format_pattern(level3_tokens)
        print(f"   {formatted}")

print("\n" + "=" * 80)
print("ANALYSIS SUMMARY")
print("=" * 80)

# Specific issues for Test 7
print("\nTest 7 Issues (Gerund as subject):")
print("- 'Running' is tagged as:", end=" ")
doc1 = nlp("Running quickly exhausted him completely.")
print(f"POS={doc1[0].pos_}, TAG={doc1[0].tag_}")
print("- 'Swimming' is tagged as:", end=" ")
doc2 = nlp("Swimming slowly relaxed her totally.")
print(f"POS={doc2[0].pos_}, TAG={doc2[0].tag_}")
print("\nPROBLEM: SpaCy is tagging gerunds at sentence start as PROPN (proper nouns) instead of VERB")
print("This causes them to be classified as NP instead of VP")

# Specific issues for Test 8
print("\nTest 8 Issues (Linking verb + ADJP):")
doc3 = nlp("She seems very happy today.")
doc4 = nlp("He looks quite tired now.")
print("- 'seems' dependencies:", [(t.text, t.dep_) for t in doc3[1].children])
print("- 'looks' dependencies:", [(t.text, t.dep_) for t in doc4[1].children])
print("\nPROBLEM: The adjectives after linking verbs are not forming consistent patterns")
print("because they're being assigned to different phrase types")

print("\n" + "=" * 80)
print("TESTING POTENTIAL FIXES")
print("=" * 80)

# Test fix 1: Check if we can identify gerunds by context
print("\nFix 1: Gerund Detection by Context")
def is_gerund_subject(token, doc):
    """Check if a token is a gerund acting as subject"""
    # Check if it's at sentence start, ends with -ing, and acts as subject
    if (token.i == 0 and 
        token.text.endswith('ing') and 
        token.dep_ in ['nsubj', 'csubj'] and
        token.head.pos_ == 'VERB'):
        return True
    return False

for text in ["Running quickly exhausted him completely.", "Swimming slowly relaxed her totally."]:
    doc = nlp(text)
    first_token = doc[0]
    print(f"- '{first_token.text}': is_gerund_subject = {is_gerund_subject(first_token, doc)}")

# Test fix 2: Custom phrase detection for linking verbs
print("\nFix 2: Linking Verb Pattern Detection")
linking_verbs = {'be', 'is', 'am', 'are', 'was', 'were', 'been', 'being',
                 'seem', 'seems', 'seemed', 'appear', 'appears', 'appeared',
                 'look', 'looks', 'looked', 'feel', 'feels', 'felt',
                 'sound', 'sounds', 'sounded', 'taste', 'tastes', 'tasted',
                 'smell', 'smells', 'smelled', 'become', 'becomes', 'became'}

def is_linking_verb_pattern(verb_token, doc):
    """Check if this is a linking verb with adjective complement"""
    if verb_token.lemma_ in linking_verbs or verb_token.text.lower() in linking_verbs:
        # Check for adjective complement
        for child in verb_token.children:
            if child.dep_ == 'acomp' and child.pos_ == 'ADJ':
                return True
    return False

for text in ["She seems very happy today.", "He looks quite tired now."]:
    doc = nlp(text)
    for token in doc:
        if token.pos_ in ['VERB', 'AUX']:
            print(f"- '{token.text}': is_linking_pattern = {is_linking_verb_pattern(token, doc)}")

print("\n" + "=" * 80)
print("PROPOSED CORRECTIONS")
print("=" * 80)

print("\nWith corrected tagging, the token sequences would be:")
print("\nTest 7 (Gerund as subject):")
print("- Text 1: Running[VP] quickly[ADVP] exhausted[VP] him[NP] completely[ADVP]")
print("- Text 2: Swimming[VP] slowly[ADVP] relaxed[VP] her[NP] totally[ADVP]")
print("- Common patterns: [ADVP] (2 occurrences), [VP] (2 occurrences)")

print("\nTest 8 (Linking verb + ADJP):")
print("- Text 1: She[NP] seems[VP] very[ADVP] happy[ADJP] today[ADVP]")  
print("- Text 2: He[NP] looks[VP] quite[ADVP] tired[ADJP] now[ADVP]")
print("- Common patterns: [NP] [VP] [ADVP] [ADJP] [ADVP] sequence")