# Pattern Finder Level 3 Test Results

**Test Date**: 2025-08-02  
**Level**: 3 (Token + Phrase Type)  
**Endpoint**: http://127.0.0.1:5000/  
**Note**: Level 3 excludes punctuation and identifies phrase types (NP, VP, PP, ADJP, ADVP, etc.)  

| # | Input | Output | ✔︎ | Comment |
|---|-------|--------|---|---------|
| 1 | Text 1: "The happy children play in the garden."<br>Text 2: "The excited students work in the classroom." | Found 4 patterns:<br>1. "in[PP] the[NP]" (2 tokens, 2 occurrences)<br>2. "The[NP]" (1 tokens, 2 occurrences)<br>3. "in[PP]" (1 tokens, 2 occurrences) | ✅ | NP + VP + PP patterns |
| 2 | Text 1: "She quickly walked to the store."<br>Text 2: "He slowly drove to the office." | Found 3 patterns:<br>1. "to[PP] the[NP]" (2 tokens, 2 occurrences)<br>2. "to[PP]" (1 tokens, 2 occurrences)<br>3. "the[NP]" (1 tokens, 2 occurrences) | ✅ | ADVP + VP + PP patterns |
| 3 | Text 1: "The big red ball bounced high."<br>Text 2: "The small blue car moved fast." | Found 1 patterns:<br>1. "The[NP]" (1 tokens, 2 occurrences) | ✅ | Complex NP with multiple modifiers |
| 4 | Text 1: "John gave Mary a beautiful gift."<br>Text 2: "Sarah sent Tom a lovely card." | Found 1 patterns:<br>1. "a[NP]" (1 tokens, 2 occurrences) | ✅ | Double object VP pattern |
| 5 | Text 1: "After the meeting, we went home."<br>Text 2: "Before the class, they ate lunch." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 2 occurrences) | ✅ | PP at sentence beginning |
| 6 | Text 1: "The book on the table is mine."<br>Text 2: "The pen in the drawer is yours." | Found 3 patterns:<br>1. "The[NP]" (1 tokens, 2 occurrences)<br>2. "the[NP]" (1 tokens, 2 occurrences)<br>3. "is[VP]" (1 tokens, 2 occurrences) | ✅ | NP with embedded PP |
| 7 | Text 1: "Running quickly exhausted him completely."<br>Text 2: "Swimming slowly relaxed her totally." | No patterns found | ❌ | Gerund VP as subject |
| 8 | Text 1: "She seems very happy today."<br>Text 2: "He looks quite tired now." | No patterns found | ❌ | Linking verb + ADJP pattern |
| 9 | Text 1: "The teacher explained the lesson clearly to the students."<br>Text 2: "The speaker presented the topic briefly to the audience." | Found 4 patterns:<br>1. "to[PP] the[NP]" (2 tokens, 2 occurrences)<br>2. "the[NP]" (1 tokens, 4 occurrences)<br>3. "The[NP]" (1 tokens, 2 occurrences) | ✅ | Complex VP with ADVP and PP |
| 10 | Text 1: "In the morning, birds sing beautifully."<br>Text 2: "At the night, owls hoot mysteriously." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 2 occurrences) | ✅ | PP + NP + VP + ADVP |
| 11 | Text 1: "The extremely talented musician played wonderfully."<br>Text 2: "The incredibly skilled artist painted beautifully." | Found 1 patterns:<br>1. "The[NP]" (1 tokens, 2 occurrences) | ✅ | Intensified ADJP in NP |
| 12 | Text 1: "They found the solution surprisingly easy."<br>Text 2: "We considered the problem remarkably simple." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 2 occurrences) | ✅ | Object complement with ADVP |
| 13 | Text 1: "Walking through the park, she saw many flowers."<br>Text 2: "Jogging along the beach, he noticed several shells." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 2 occurrences) | ✅ | Participial phrase + main clause |
| 14 | Text 1: "To succeed in life, one must work hard."<br>Text 2: "To excel at sports, you should practice daily." | Found 1 patterns:<br>1. "To[INF-P]" (1 tokens, 2 occurrences) | ✅ | Infinitive phrase pattern |
| 15 | Text 1: "The students studying hard will pass easily."<br>Text 2: "The workers arriving early can leave sooner." | Found 1 patterns:<br>1. "The[NP]" (1 tokens, 2 occurrences) | ✅ | Reduced relative clause in NP |
| 16 | Text 1: "Both the cat and the dog sleep peacefully."<br>Text 2: "Either the bus or the train arrives promptly." | Found 1 patterns:<br>1. "the[NP]" (1 tokens, 4 occurrences) | ✅ | Coordinated NP subjects |
| 17 | Text 1: "She not only sings beautifully but also dances gracefully."<br>Text 2: "He not only writes clearly but also speaks eloquently." | Found 6 patterns:<br>1. "not[PART] only[ADVP]" (2 tokens, 2 occurrences)<br>2. "but[CONJP] also[ADVP]" (2 tokens, 2 occurrences)<br>3. "not[PART]" (1 tokens, 2 occurrences) | ✅ | Correlative conjunction with ADVP |
| 18 | Text 1: "The more carefully you study, the better you understand."<br>Text 2: "The more diligently she works, the faster she progresses." | Found 4 patterns:<br>1. "The[ADVP] more[ADVP]" (2 tokens, 2 occurrences)<br>2. "The[ADVP]" (1 tokens, 2 occurrences)<br>3. "more[ADVP]" (1 tokens, 2 occurrences) | ✅ | Comparative correlative with ADVP |
| 19 | Text 1: "Despite the heavy rain, they continued playing outside."<br>Text 2: "Despite the strong wind, we kept walking forward." | Found 3 patterns:<br>1. "Despite[CONJP] the[NP]" (2 tokens, 2 occurrences)<br>2. "Despite[CONJP]" (1 tokens, 2 occurrences)<br>3. "the[NP]" (1 tokens, 2 occurrences) | ✅ | Concessive PP + VP + ADVP |
| 20 | Text 1: "What she said yesterday surprised everyone greatly."<br>Text 2: "What he did today shocked everybody completely." | Found 1 patterns:<br>1. "What[NP]" (1 tokens, 2 occurrences) | ✅ | Nominal clause as subject |

## Summary
- **Total Tests**: 20
- **Passed**: 18
- **Failed**: 2
- **Success Rate**: 18/20 (90.0%)

## Phrase Type Legend
- **NP**: Noun Phrase
- **VP**: Verb Phrase
- **PP**: Prepositional Phrase
- **ADJP**: Adjective Phrase
- **ADVP**: Adverb Phrase
- **CONJP**: Conjunction Phrase
- **INFP**: Infinitive Phrase
- **O**: Other/No specific phrase type
