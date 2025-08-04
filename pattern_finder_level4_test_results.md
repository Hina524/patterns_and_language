# Pattern Finder Level 4 Test Results

**Test Date**: 2025-08-04  
**Level**: 4 (Token + POS + Phrase Type)  
**Endpoint**: http://127.0.0.1:5000/api/find-patterns  
**Note**: Level 4 includes full linguistic analysis with tokens, part-of-speech tags, and phrase types  

| # | Input | Output | ✔︎ | Comment |
|---|-------|--------|---|---------|
| 1 | Text 1: "The happy children play in the garden."<br>Text 2: "The excited students work in the classroom." | Found 7 patterns:<br>1. "in(ADP)[PP] the(DET)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>... and 4 more | ✅ | NP + VP + PP patterns |
| 2 | Text 1: "She quickly walked to the store."<br>Text 2: "He slowly drove to the office." | Found 6 patterns:<br>1. "to(ADP)[PP] the(DET)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. "to(ADP)[PP]" (1 tokens, 2 occurrences)<br>... and 3 more | ✅ | ADVP + VP + PP patterns |
| 3 | Text 1: "The big red ball bounced high."<br>Text 2: "The small blue car moved fast." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Complex NP with multiple modifiers |
| 4 | Text 1: "John gave Mary a beautiful gift."<br>Text 2: "Sarah sent Tom a lovely card." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. "a(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Double object VP pattern |
| 5 | Text 1: "After the meeting, we went home."<br>Text 2: "Before the class, they ate lunch." | Found 5 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ",(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 2 more | ✅ | PP at sentence beginning |
| 6 | Text 1: "The book on the table is mine."<br>Text 2: "The pen in the drawer is yours." | Found 6 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>3. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>... and 3 more | ✅ | NP with embedded PP |
| 7 | Text 1: "Running quickly exhausted him completely."<br>Text 2: "Swimming slowly relaxed her totally." | Found 3 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[ADVP]" (1 tokens, 2 occurrences) | ✅ | Gerund VP as subject |
| 8 | Text 1: "She seems very happy today."<br>Text 2: "He looks quite tired now." | Found 3 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[ADVP]" (1 tokens, 2 occurrences) | ✅ | Linking verb + ADJP pattern |
| 9 | Text 1: "The teacher explained the lesson clearly to the students."<br>Text 2: "The speaker presented the topic briefly to the audience." | Found 7 patterns:<br>1. "to(ADP)[PP] the(DET)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. "the(DET)[NP]" (1 tokens, 4 occurrences)<br>... and 4 more | ✅ | Complex VP with ADVP and PP |
| 10 | Text 1: "In the morning, birds sing beautifully."<br>Text 2: "At the night, owls hoot mysteriously." | Found 7 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>3. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>... and 4 more | ✅ | PP + NP + VP + ADVP |
| 11 | Text 1: "The extremely talented musician played wonderfully."<br>Text 2: "The incredibly skilled artist painted beautifully." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Intensified ADJP in NP |
| 12 | Text 1: "They found the solution surprisingly easy."<br>Text 2: "We considered the problem remarkably simple." | Found 2 patterns:<br>1. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>2. ".(PUNCT)[O]" (1 tokens, 2 occurrences) | ✅ | Object complement with ADVP |
| 13 | Text 1: "Walking through the park, she saw many flowers."<br>Text 2: "Jogging along the beach, he noticed several shells." | Found 7 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. "the(DET)[NP]" (1 tokens, 2 occurrences)<br>... and 4 more | ✅ | Participial phrase + main clause |
| 14 | Text 1: "To succeed in life, one must work hard."<br>Text 2: "To excel at sports, you should practice daily." | Found 7 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>2. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>3. "To(PART)[INF-P]" (1 tokens, 2 occurrences)<br>... and 4 more | ✅ | Infinitive phrase pattern |
| 15 | Text 1: "The students studying hard will pass easily."<br>Text 2: "The workers arriving early can leave sooner." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "The(DET)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Reduced relative clause in NP |
| 16 | Text 1: "Both the cat and the dog sleep peacefully."<br>Text 2: "Either the bus or the train arrives promptly." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "the(DET)[NP]" (1 tokens, 4 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Coordinated NP subjects |
| 17 | Text 1: "She not only sings beautifully but also dances gracefully."<br>Text 2: "He not only writes clearly but also speaks eloquently." | Found 9 patterns:<br>1. "not(PART)[PART] only(ADV)[ADVP]" (2 tokens, 2 occurrences)<br>2. "but(CCONJ)[CONJP] also(ADV)[ADVP]" (2 tokens, 2 occurrences)<br>3. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>... and 6 more | ✅ | Correlative conjunction with ADVP |
| 18 | Text 1: "The more carefully you study, the better you understand."<br>Text 2: "The more diligently she works, the faster she progresses." | Found 12 patterns:<br>1. ",(PUNCT)[O] ,(PUNCT)[VP] the(PRON)[ADVP]" (3 tokens, 2 occurrences)<br>2. "The(PRON)[ADVP] more(ADV)[ADVP]" (2 tokens, 2 occurrences)<br>3. ",(PUNCT)[O] ,(PUNCT)[VP]" (2 tokens, 2 occurrences)<br>... and 9 more | ✅ | Comparative correlative with ADVP |
| 19 | Text 1: "Despite the heavy rain, they continued playing outside."<br>Text 2: "Despite the strong wind, we kept walking forward." | Found 9 patterns:<br>1. "Despite(SCONJ)[CONJP] the(DET)[NP]" (2 tokens, 2 occurrences)<br>2. ",(PUNCT)[O] ,(PUNCT)[NP]" (2 tokens, 2 occurrences)<br>3. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>... and 6 more | ✅ | Concessive PP + VP + ADVP |
| 20 | Text 1: "What she said yesterday surprised everyone greatly."<br>Text 2: "What he did today shocked everybody completely." | Found 4 patterns:<br>1. ".(PUNCT)[O] .(PUNCT)[ADVP]" (2 tokens, 2 occurrences)<br>2. "What(PRON)[NP]" (1 tokens, 2 occurrences)<br>3. ".(PUNCT)[O]" (1 tokens, 2 occurrences)<br>... and 1 more | ✅ | Nominal clause as subject |

## Summary
- **Total Tests**: 20
- **Passed**: 20
- **Failed**: 0
- **Success Rate**: 20/20 (100.0%)

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
