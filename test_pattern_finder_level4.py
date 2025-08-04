#!/usr/bin/env python3
import requests
import json
import time

def test_pattern_finder_level4():
    """Test Pattern Finder with Level 4 (Token + POS + Phrase Type)"""
    
    # API endpoint
    url = "http://127.0.0.1:5000/api/find-patterns"
    
    # Test cases - same as Level 3 but expecting Level 4 output format
    test_cases = [
        {
            "number": 1,
            "texts": [
                "The happy children play in the garden.",
                "The excited students work in the classroom."
            ],
            "description": "NP + VP + PP patterns"
        },
        {
            "number": 2,
            "texts": [
                "She quickly walked to the store.",
                "He slowly drove to the office."
            ],
            "description": "ADVP + VP + PP patterns"
        },
        {
            "number": 3,
            "texts": [
                "The big red ball bounced high.",
                "The small blue car moved fast."
            ],
            "description": "Complex NP with multiple modifiers"
        },
        {
            "number": 4,
            "texts": [
                "John gave Mary a beautiful gift.",
                "Sarah sent Tom a lovely card."
            ],
            "description": "Double object VP pattern"
        },
        {
            "number": 5,
            "texts": [
                "After the meeting, we went home.",
                "Before the class, they ate lunch."
            ],
            "description": "PP at sentence beginning"
        },
        {
            "number": 6,
            "texts": [
                "The book on the table is mine.",
                "The pen in the drawer is yours."
            ],
            "description": "NP with embedded PP"
        },
        {
            "number": 7,
            "texts": [
                "Running quickly exhausted him completely.",
                "Swimming slowly relaxed her totally."
            ],
            "description": "Gerund VP as subject"
        },
        {
            "number": 8,
            "texts": [
                "She seems very happy today.",
                "He looks quite tired now."
            ],
            "description": "Linking verb + ADJP pattern"
        },
        {
            "number": 9,
            "texts": [
                "The teacher explained the lesson clearly to the students.",
                "The speaker presented the topic briefly to the audience."
            ],
            "description": "Complex VP with ADVP and PP"
        },
        {
            "number": 10,
            "texts": [
                "In the morning, birds sing beautifully.",
                "At the night, owls hoot mysteriously."
            ],
            "description": "PP + NP + VP + ADVP"
        },
        {
            "number": 11,
            "texts": [
                "The extremely talented musician played wonderfully.",
                "The incredibly skilled artist painted beautifully."
            ],
            "description": "Intensified ADJP in NP"
        },
        {
            "number": 12,
            "texts": [
                "They found the solution surprisingly easy.",
                "We considered the problem remarkably simple."
            ],
            "description": "Object complement with ADVP"
        },
        {
            "number": 13,
            "texts": [
                "Walking through the park, she saw many flowers.",
                "Jogging along the beach, he noticed several shells."
            ],
            "description": "Participial phrase + main clause"
        },
        {
            "number": 14,
            "texts": [
                "To succeed in life, one must work hard.",
                "To excel at sports, you should practice daily."
            ],
            "description": "Infinitive phrase pattern"
        },
        {
            "number": 15,
            "texts": [
                "The students studying hard will pass easily.",
                "The workers arriving early can leave sooner."
            ],
            "description": "Reduced relative clause in NP"
        },
        {
            "number": 16,
            "texts": [
                "Both the cat and the dog sleep peacefully.",
                "Either the bus or the train arrives promptly."
            ],
            "description": "Coordinated NP subjects"
        },
        {
            "number": 17,
            "texts": [
                "She not only sings beautifully but also dances gracefully.",
                "He not only writes clearly but also speaks eloquently."
            ],
            "description": "Correlative conjunction with ADVP"
        },
        {
            "number": 18,
            "texts": [
                "The more carefully you study, the better you understand.",
                "The more diligently she works, the faster she progresses."
            ],
            "description": "Comparative correlative with ADVP"
        },
        {
            "number": 19,
            "texts": [
                "Despite the heavy rain, they continued playing outside.",
                "Despite the strong wind, we kept walking forward."
            ],
            "description": "Concessive PP + VP + ADVP"
        },
        {
            "number": 20,
            "texts": [
                "What she said yesterday surprised everyone greatly.",
                "What he did today shocked everybody completely."
            ],
            "description": "Nominal clause as subject"
        }
    ]
    
    results = []
    passed = 0
    
    print("Testing Pattern Finder Level 4 (Token + POS + Phrase Type)...")
    print("=" * 70)
    
    for test in test_cases:
        test_num = test["number"]
        print(f"\nTest {test_num}: {test['description']}")
        print("-" * 50)
        
        # Make request
        payload = {
            "texts": test["texts"],
            "level": 4  # Level 4 analysis
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            print(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Error: HTTP {response.status_code}")
                print(f"Response text: {response.text[:500]}")
                results.append({
                    "number": test_num,
                    "description": test["description"],
                    "texts": test["texts"],
                    "patterns": [],
                    "passed": False,
                    "error": f"HTTP {response.status_code}"
                })
                continue
                
            data = response.json()
            
            if data.get("success", False):
                patterns = data.get("patterns", [])
                
                # Format result
                result = {
                    "number": test_num,
                    "description": test["description"],
                    "texts": test["texts"],
                    "patterns": patterns,
                    "passed": len(patterns) > 0
                }
                
                # Print patterns found
                if patterns:
                    print(f"Found {len(patterns)} patterns:")
                    for i, p in enumerate(patterns[:5], 1):  # Show first 5 patterns
                        print(f"  {i}. \"{p['pattern']}\" ({p['length']} tokens, {p['count']} occurrences)")
                    if len(patterns) > 5:
                        print(f"  ... and {len(patterns) - 5} more patterns")
                    passed += 1
                else:
                    print("No patterns found")
                    
                results.append(result)
                
            else:
                print(f"Error: {data.get('error', 'Unknown error')}")
                results.append({
                    "number": test_num,
                    "description": test["description"],
                    "texts": test["texts"],
                    "patterns": [],
                    "passed": False,
                    "error": data.get('error', 'Unknown error')
                })
                
        except Exception as e:
            print(f"Request failed: {str(e)}")
            results.append({
                "number": test_num,
                "description": test["description"],
                "texts": test["texts"],
                "patterns": [],
                "passed": False,
                "error": str(e)
            })
    
    print("\n" + "=" * 70)
    print(f"Summary: {passed}/{len(test_cases)} tests passed ({passed/len(test_cases)*100:.1f}%)")
    
    # Generate markdown report
    generate_markdown_report(results, len(test_cases), passed)

def generate_markdown_report(results, total_tests, passed_tests):
    """Generate a markdown report of the test results"""
    
    report = """# Pattern Finder Level 4 Test Results

**Test Date**: 2025-08-04  
**Level**: 4 (Token + POS + Phrase Type)  
**Endpoint**: http://127.0.0.1:5000/api/find-patterns  
**Note**: Level 4 includes full linguistic analysis with tokens, part-of-speech tags, and phrase types  

| # | Input | Output | ✔︎ | Comment |
|---|-------|--------|---|---------|
"""
    
    for result in results:
        num = result["number"]
        texts = result["texts"]
        patterns = result.get("patterns", [])
        passed = result["passed"]
        description = result["description"]
        error = result.get("error", "")
        
        # Format input texts
        input_text = f"Text 1: \"{texts[0]}\"<br>Text 2: \"{texts[1]}\""
        
        # Format output
        if error:
            output = f"Error: {error}"
        elif patterns:
            output = f"Found {len(patterns)} patterns:"
            for i, p in enumerate(patterns[:3], 1):  # Show first 3 patterns
                output += f"<br>{i}. \"{p['pattern']}\" ({p['length']} tokens, {p['count']} occurrences)"
            if len(patterns) > 3:
                output += f"<br>... and {len(patterns) - 3} more"
        else:
            output = "No patterns found"
        
        # Pass/fail mark
        mark = "✅" if passed else "❌"
        
        # Add row to table
        report += f"| {num} | {input_text} | {output} | {mark} | {description} |\n"
    
    # Add summary
    report += f"""
## Summary
- **Total Tests**: {total_tests}
- **Passed**: {passed_tests}
- **Failed**: {total_tests - passed_tests}
- **Success Rate**: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)

## Output Format Explanation
Level 4 format: `token(POS)[phrase]`
- **token**: The actual word or token
- **POS**: Part-of-speech tag (NOUN, VERB, ADJ, etc.)
- **phrase**: Phrase type (NP, VP, PP, etc.)

## Part-of-Speech Tags
- **DET**: Determiner (the, a, an)
- **NOUN**: Noun
- **VERB**: Verb
- **ADJ**: Adjective
- **ADV**: Adverb
- **ADP**: Adposition (preposition/postposition)
- **PRON**: Pronoun
- **AUX**: Auxiliary verb
- **CCONJ**: Coordinating conjunction
- **SCONJ**: Subordinating conjunction
- **PART**: Particle
- **PUNCT**: Punctuation

## Phrase Type Legend
- **NP**: Noun Phrase
- **VP**: Verb Phrase
- **PP**: Prepositional Phrase
- **ADJP**: Adjective Phrase
- **ADVP**: Adverb Phrase
- **CONJP**: Conjunction Phrase
- **INF-P**: Infinitive Phrase
- **DP**: Determiner Phrase
- **PART**: Particle
- **NUM**: Number
- **O**: Other/No specific phrase type
"""
    
    # Write to file
    with open("pattern_finder_level4_test_results.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\nReport saved to pattern_finder_level4_test_results.md")

if __name__ == "__main__":
    # Wait for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    test_pattern_finder_level4()