# Pattern Finder Level 2 Test Results

**Test Date**: 2025-08-02  
**Level**: 2 (Token + POS)  
**Endpoint**: http://127.0.0.1:5000/  

| # | Input | Output | ✔︎ | Comment |
|---|-------|--------|---|---------|
| 1 | Text 1: "The cat sits on the mat."<br>Text 2: "The dog sits on the floor." | Found 3 patterns:<br>1. "sits(VERB) on(ADP) the(DET)" (3 tokens, 2 occurrences)<br>2. "sits(VERB) on(ADP)" (2 tokens, 2 occurrences)<br>3. "on(ADP) the(DET)" (2 tokens, 2 occurrences) | ✅ | Common pattern with determiner, noun, verb, preposition |
| 2 | Text 1: "She quickly runs to school."<br>Text 2: "He quickly walks to work." | Found 2 patterns:<br>1. "quickly(ADV)" (1 token, 2 occurrences)<br>2. ".(PUNCT)" (1 token, 2 occurrences) | ✅ | Pattern with adverb modifying verb |
| 3 | Text 1: "I love eating pizza and pasta."<br>Text 2: "We love eating burgers and fries." | Found 3 patterns:<br>1. "love(VERB) eating(VERB)" (2 tokens, 2 occurrences)<br>2. "love(VERB)" (1 token, 2 occurrences)<br>3. "eating(VERB)" (1 token, 2 occurrences) | ✅ | Pattern with gerund and coordinated nouns |
| 4 | Text 1: "The beautiful garden blooms in spring."<br>Text 2: "The beautiful park shines in summer." | Found 3 patterns:<br>1. "The(DET) beautiful(ADJ)" (2 tokens, 2 occurrences)<br>2. "The(DET)" (1 token, 2 occurrences)<br>3. "beautiful(ADJ)" (1 token, 2 occurrences) | ✅ | Pattern with adjective-noun combination |
| 5 | Text 1: "Can you help me with this?"<br>Text 2: "Can you assist me with that?" | Found 3 patterns:<br>1. "Can(AUX) you(PRON)" (2 tokens, 2 occurrences)<br>2. "me(PRON) with(ADP)" (2 tokens, 2 occurrences)<br>3. "Can(AUX)" (1 token, 2 occurrences) | ✅ | Modal auxiliary pattern |
| 6 | Text 1: "She has been studying all day."<br>Text 2: "He has been working all night." | Found 3 patterns:<br>1. "has(AUX) been(AUX)" (2 tokens, 2 occurrences)<br>2. "has(AUX)" (1 token, 2 occurrences)<br>3. "been(AUX)" (1 token, 2 occurrences) | ✅ | Present perfect continuous pattern |
| 7 | Text 1: "If it rains, we will stay home."<br>Text 2: "If it snows, we will stay inside." | Found 3 patterns:<br>1. ",(PUNCT) we(PRON) will(AUX) stay(VERB)" (4 tokens, 2 occurrences)<br>2. ",(PUNCT) we(PRON) will(AUX)" (3 tokens, 2 occurrences)<br>3. "we(PRON) will(AUX) stay(VERB)" (3 tokens, 2 occurrences) | ✅ | Conditional sentence pattern |
| 8 | Text 1: "The book that I read was interesting."<br>Text 2: "The movie that I watched was boring." | Found 3 patterns:<br>1. "that(PRON) I(PRON)" (2 tokens, 2 occurrences)<br>2. "The(DET)" (1 token, 2 occurrences)<br>3. "that(PRON)" (1 token, 2 occurrences) | ✅ | Relative clause pattern |
| 9 | Text 1: "Running is good for health."<br>Text 2: "Swimming is good for fitness." | Found 3 patterns:<br>1. "is(AUX) good(ADJ) for(ADP)" (3 tokens, 2 occurrences)<br>2. "is(AUX) good(ADJ)" (2 tokens, 2 occurrences)<br>3. "good(ADJ) for(ADP)" (2 tokens, 2 occurrences) | ✅ | Gerund as subject pattern |
| 10 | Text 1: "She told me to wait here."<br>Text 2: "He asked me to wait there." | Found 3 patterns:<br>1. "me(PRON) to(PART) wait(VERB)" (3 tokens, 2 occurrences)<br>2. "me(PRON) to(PART)" (2 tokens, 2 occurrences)<br>3. "to(PART) wait(VERB)" (2 tokens, 2 occurrences) | ✅ | Infinitive phrase pattern |
| 11 | Text 1: "Not only did she sing, but she also danced."<br>Text 2: "Not only did he play, but he also coached." | Found 3 patterns:<br>1. "Not(PART) only(ADV) did(AUX)" (3 tokens, 2 occurrences)<br>2. "Not(PART) only(ADV)" (2 tokens, 2 occurrences)<br>3. "only(ADV) did(AUX)" (2 tokens, 2 occurrences) | ✅ | Complex correlative conjunction pattern |
| 12 | Text 1: "The more you practice, the better you become."<br>Text 2: "The more you study, the smarter you become." | Found 3 patterns:<br>1. "The(PRON) more(ADV) you(PRON)" (3 tokens, 2 occurrences)<br>2. "you(PRON) become(VERB) .(PUNCT)" (3 tokens, 2 occurrences)<br>3. "The(PRON) more(ADV)" (2 tokens, 2 occurrences) | ✅ | Comparative correlative pattern |
| 13 | Text 1: "There are many books on the shelf."<br>Text 2: "There are many toys on the floor." | Found 3 patterns:<br>1. "There(PRON) are(VERB) many(ADJ)" (3 tokens, 2 occurrences)<br>2. "There(PRON) are(VERB)" (2 tokens, 2 occurrences)<br>3. "are(VERB) many(ADJ)" (2 tokens, 2 occurrences) | ✅ | Existential 'there' pattern |
| 14 | Text 1: "What a beautiful day it is!"<br>Text 2: "What a wonderful time it was!" | Found 3 patterns:<br>1. "What(PRON) a(DET)" (2 tokens, 2 occurrences)<br>2. "What(PRON)" (1 token, 2 occurrences)<br>3. "a(DET)" (1 token, 2 occurrences) | ✅ | Exclamatory sentence pattern |
| 15 | Text 1: "John, my best friend, lives nearby."<br>Text 2: "Mary, my dear sister, works nearby." | Found 3 patterns:<br>1. ",(PUNCT) my(PRON)" (2 tokens, 2 occurrences)<br>2. "nearby(ADV) .(PUNCT)" (2 tokens, 2 occurrences)<br>3. ",(PUNCT)" (1 token, 4 occurrences) | ✅ | Appositive phrase pattern |
| 16 | Text 1: "Having finished the work, she went home."<br>Text 2: "Having completed the task, he went away." | Found 3 patterns:<br>1. "Having(AUX)" (1 token, 2 occurrences)<br>2. "the(DET)" (1 token, 2 occurrences)<br>3. ",(PUNCT)" (1 token, 2 occurrences) | ✅ | Participial phrase pattern |
| 17 | Text 1: "It is important to exercise regularly."<br>Text 2: "It is necessary to study consistently." | Found 3 patterns:<br>1. "It(PRON) is(AUX)" (2 tokens, 2 occurrences)<br>2. "It(PRON)" (1 token, 2 occurrences)<br>3. "is(AUX)" (1 token, 2 occurrences) | ✅ | Extraposition pattern |
| 18 | Text 1: "The faster he runs, the more tired he gets."<br>Text 2: "The harder she works, the more successful she becomes." | Found 3 patterns:<br>1. ",(PUNCT) the(PRON) more(ADV)" (3 tokens, 2 occurrences)<br>2. ",(PUNCT) the(PRON)" (2 tokens, 2 occurrences)<br>3. "the(PRON) more(ADV)" (2 tokens, 2 occurrences) | ✅ | Complex comparative pattern |
| 19 | Text 1: "Either you come with us or stay here alone."<br>Text 2: "Either we go together or stay here together." | Found 3 patterns:<br>1. "or(CCONJ) stay(VERB) here(ADV)" (3 tokens, 2 occurrences)<br>2. "or(CCONJ) stay(VERB)" (2 tokens, 2 occurrences)<br>3. "stay(VERB) here(ADV)" (2 tokens, 2 occurrences) | ✅ | Either-or coordination pattern |
| 20 | Text 1: "Despite being tired, she continued working hard."<br>Text 2: "Despite being sick, he continued studying hard." | Found 3 patterns:<br>1. "Despite(SCONJ) being(AUX)" (2 tokens, 2 occurrences)<br>2. "hard(ADV) .(PUNCT)" (2 tokens, 2 occurrences)<br>3. "Despite(SCONJ)" (1 token, 2 occurrences) | ✅ | Concessive phrase pattern |

## Summary
- **Total Tests**: 20
- **Passed**: 20
- **Failed**: 0
- **Success Rate**: 20/20 (100.0%)
