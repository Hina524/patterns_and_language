#!/usr/bin/env python3
import os
import sys
import glob
from collections import defaultdict
import argparse
import spacy
import json

class PatternFinder:
    def __init__(self, level=1):
        self.level = level
        self.nlp = None
        if level > 1:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except:
                print("Please install spacy and en_core_web_sm: python -m spacy download en_core_web_sm")
                sys.exit(1)
        
        # Linking verbs for special pattern detection
        self.linking_verbs = {
            'be', 'is', 'am', 'are', 'was', 'were', 'been', 'being',
            'seem', 'seems', 'seemed', 'appear', 'appears', 'appeared',
            'look', 'looks', 'looked', 'feel', 'feels', 'felt',
            'sound', 'sounds', 'sounded', 'taste', 'tastes', 'tasted',
            'smell', 'smells', 'smelled', 'become', 'becomes', 'became',
            'remain', 'remains', 'remained', 'stay', 'stays', 'stayed',
            'grow', 'grows', 'grew', 'turn', 'turns', 'turned'
        }
    
    def get_files_from_folder(self, folder):
        """Get all text files from a folder"""
        pattern = os.path.join(folder, '*.txt')
        files = glob.glob(pattern)
        if not files:
            print(f"No text files found in {folder}")
            sys.exit(1)
        return files
    
    def read_texts(self, files):
        """Read all text files"""
        texts = []
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        texts.append((file_path, content))
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        return texts
    
    def _is_gerund_subject(self, token, doc):
        """Check if a token is a gerund acting as subject"""
        # Check multiple conditions for gerund detection
        if token.text.endswith('ing'):
            # Case 1: Token is marked as subject dependency
            if token.dep_ in ['nsubj', 'csubj']:
                return True
            
            # Case 2: Token is at sentence start and followed by adverb then verb
            if token.i == 0 and len(doc) > 2:
                # Check if next tokens form gerund phrase pattern
                if (token.i + 1 < len(doc) and 
                    doc[token.i + 1].pos_ == 'ADV' and
                    token.i + 2 < len(doc) and
                    doc[token.i + 2].pos_ == 'VERB'):
                    return True
            
            # Case 3: SpaCy mistakenly tagged as PROPN but acts as subject
            if (token.pos_ == 'PROPN' and 
                token.dep_ == 'nsubj' and
                token.i == 0):
                return True
        
        return False
    
    def _correct_token_pos(self, token, doc):
        """Correct common spaCy POS tagging errors"""
        # Fix gerunds tagged as proper nouns
        if (token.pos_ == 'PROPN' and 
            token.text.endswith('ing') and
            self._is_gerund_subject(token, doc)):
            return 'VERB'
        
        return token.pos_
    
    def _is_linking_verb_with_adjective(self, verb_token, doc):
        """Check if this is a linking verb followed by adjective complement"""
        if verb_token.lemma_ in self.linking_verbs or verb_token.text.lower() in self.linking_verbs:
            # Look for adjective complements
            for child in verb_token.children:
                # Check for various adjective complement dependencies
                if (child.dep_ in ['acomp', 'oprd', 'attr'] and 
                    child.pos_ == 'ADJ'):
                    return True
                # Sometimes the adjective is marked as 'xcomp'
                if child.dep_ == 'xcomp' and child.pos_ == 'ADJ':
                    return True
        return False
    
    def tokenize(self, text):
        """Tokenize text based on level"""
        if self.level == 1:
            # Simple token level
            if self.nlp:
                doc = self.nlp(text)
                return [token.text for token in doc if not token.is_space]
            else:
                # Fallback to simple split
                return text.split()
        
        elif self.level == 2:
            # Token + POS
            doc = self.nlp(text)
            return [(token.text, token.pos_) for token in doc if not token.is_space]
        
        elif self.level == 3:
            # Token + phrase (exclude punctuation)
            doc = self.nlp(text)
            phrase_map = self._build_phrase_map(doc)
            tokens = []
            for token in doc:
                if token.is_space or token.pos_ == 'PUNCT':
                    continue  # Skip punctuation in phrase analysis
                phrase_type = self.get_phrase_type(token, doc, phrase_map)
                tokens.append((token.text, phrase_type))
            return tokens
        
        elif self.level == 4:
            # Token + POS + phrase
            doc = self.nlp(text)
            phrase_map = self._build_phrase_map(doc)
            tokens = []
            for token in doc:
                if token.is_space:
                    continue
                if token.pos_ == 'PUNCT':
                    # For punctuation, only include POS, no phrase type
                    tokens.append((token.text, token.pos_, 'O'))
                else:
                    phrase_type = self.get_phrase_type(token, doc, phrase_map)
                tokens.append((token.text, token.pos_, phrase_type))
            return tokens
    
    def get_phrase_type(self, token, doc, phrase_map=None):
        """Get phrase type for a token using comprehensive spaCy analysis"""
        
        # Build phrase map if not provided
        if phrase_map is None:
            phrase_map = self._build_phrase_map(doc)
        
        # Return the phrase type for this token
        return phrase_map.get(token.i, 'O')
    
    def _build_phrase_map(self, doc):
        """Build a comprehensive map of phrase types for all tokens with accuracy fixes"""
        phrase_map = {}
        
        # Step 0: Handle gerund subjects FIRST (before noun chunks)
        for token in doc:
            if self._is_gerund_subject(token, doc):
                # Mark gerund as VP
                phrase_map[token.i] = 'VP'
        
        # Step 1: Mark noun chunks (but don't overwrite gerunds)
        for chunk in doc.noun_chunks:
            for i in range(chunk.start, chunk.end):
                if i not in phrase_map:  # Don't overwrite gerunds
                    phrase_map[i] = 'NP'
        
        # Step 2: Identify infinitive phrases (to + verb) - BEFORE verb phrases
        for token in doc:
            if self._is_infinitive_marker(token, doc) and token.i not in phrase_map:
                inf_tokens = self._get_infinitive_phrase_tokens(token, doc)
                for i in inf_tokens:
                    if i not in phrase_map:
                        phrase_map[i] = 'INF-P'
        
        # Step 3: Identify verb phrases (with linking verb handling)
        for token in doc:
            if token.pos_ in ['VERB', 'AUX'] and token.i not in phrase_map:
                # Check if it's a linking verb with adjective
                if self._is_linking_verb_with_adjective(token, doc):
                    # Only mark the verb itself as VP, let adjectives be handled separately
                    phrase_map[token.i] = 'VP'
                else:
                    vp_tokens = self._get_verb_phrase_tokens(token, doc)
                    for i in vp_tokens:
                        if i not in phrase_map:
                            phrase_map[i] = 'VP'
        
        # Step 4: Identify prepositional phrases
        for token in doc:
            if token.pos_ == 'ADP' and token.i not in phrase_map:
                pp_tokens = self._get_prepositional_phrase_tokens(token, doc)
                for i in pp_tokens:
                    if i not in phrase_map:  # Don't overwrite existing phrases
                        phrase_map[i] = 'PP'
        
        # Step 5: Identify adjective phrases (with special handling for linking verb complements)
        for token in doc:
            if token.pos_ == 'ADJ' and token.i not in phrase_map:
                # Check if this adjective is a complement to a linking verb
                if token.dep_ in ['acomp', 'oprd'] and token.head.pos_ == 'VERB':
                    # This is an adjective complement - mark it and its modifiers as ADJP
                    adjp_tokens = self._get_adjective_phrase_tokens(token, doc)
                    for i in adjp_tokens:
                        if i not in phrase_map:
                            phrase_map[i] = 'ADJP'
                else:
                    # Regular adjective phrase
                    adjp_tokens = self._get_adjective_phrase_tokens(token, doc)
                    for i in adjp_tokens:
                        if i not in phrase_map:
                            phrase_map[i] = 'ADJP'
        
        # Step 6: Identify adverb phrases (with special handling for time/place adverbs)
        for token in doc:
            if token.pos_ == 'ADV' and token.i not in phrase_map:
                advp_tokens = self._get_adverb_phrase_tokens(token, doc)
                for i in advp_tokens:
                    if i not in phrase_map:
                        phrase_map[i] = 'ADVP'
        
        # Step 7: Handle remaining tokens with specific rules
        for token in doc:
            if token.i not in phrase_map:
                phrase_map[token.i] = self._classify_remaining_token(token, doc)
        
        return phrase_map
    
    def _get_verb_phrase_tokens(self, verb, doc):
        """Get all tokens that belong to a verb phrase headed by this verb"""
        vp_tokens = {verb.i}
        
        # Include auxiliary verbs and particles
        for child in verb.children:
            if child.dep_ in ['aux', 'auxpass', 'neg', 'prt']:
                vp_tokens.add(child.i)
        
        # Include infinitive marker 'to' when it's part of infinitive
        if verb.dep_ == 'xcomp' and verb.head.pos_ == 'VERB':
            # Look for 'to' before this verb
            for i in range(max(0, verb.i - 2), verb.i):
                if doc[i].text.lower() == 'to' and doc[i].dep_ == 'aux':
                    vp_tokens.add(i)
        
        return vp_tokens
    
    def _get_prepositional_phrase_tokens(self, prep, doc):
        """Get all tokens that belong to a prepositional phrase headed by this preposition"""
        pp_tokens = {prep.i}
        
        # Include the object of the preposition and its modifiers
        for child in prep.children:
            if child.dep_ == 'pobj':
                # Add the object and its subtree (but avoid noun chunks already marked)
                pp_tokens.add(child.i)
                for desc in child.subtree:
                    if desc.i != child.i:  # Don't double-add the head
                        pp_tokens.add(desc.i)
        
        return pp_tokens
    
    def _get_adjective_phrase_tokens(self, adj, doc):
        """Get all tokens that belong to an adjective phrase headed by this adjective"""
        adjp_tokens = {adj.i}
        
        # Include adverbs modifying the adjective (including intensifiers)
        for child in adj.children:
            if child.dep_ in ['advmod', 'npadvmod']:
                adjp_tokens.add(child.i)
                # Also include children of the adverb (for multi-word intensifiers)
                for grandchild in child.children:
                    if grandchild.dep_ == 'advmod':
                        adjp_tokens.add(grandchild.i)
        
        # If this adjective modifies another adjective, include it in the same phrase
        if adj.head.pos_ == 'ADJ' and adj.dep_ == 'amod':
            adjp_tokens.add(adj.head.i)
        
        return adjp_tokens
    
    def _get_adverb_phrase_tokens(self, adv, doc):
        """Get all tokens that belong to an adverb phrase headed by this adverb"""
        advp_tokens = {adv.i}
        
        # Include modifying adverbs
        for child in adv.children:
            if child.dep_ == 'advmod':
                advp_tokens.add(child.i)
        
        # Special handling for time/place nouns acting as adverbs
        if (adv.pos_ == 'NOUN' and 
            adv.dep_ in ['npadvmod', 'tmod'] and
            adv.text.lower() in ['today', 'tomorrow', 'yesterday', 'now', 'then', 'here', 'there']):
            # These should be treated as ADVP
            return advp_tokens
        
        return advp_tokens
    
    def _is_infinitive_marker(self, token, doc):
        """Check if this token is an infinitive marker 'to'"""
        # Check for 'to' + verb pattern
        if (token.pos_ == 'PART' and 
            token.tag_ == 'TO' and 
            token.text.lower() == 'to'):
            
            # Check if followed by a verb (infinitive structure)
            if token.i + 1 < len(doc):
                next_token = doc[token.i + 1]
                if next_token.pos_ == 'VERB' and next_token.tag_ == 'VB':
                    return True
            
            # Check if it's marked as auxiliary to a verb (xcomp relation)
            if token.dep_ == 'aux' and token.head.pos_ == 'VERB':
                return True
                
        return False
    
    def _get_infinitive_phrase_tokens(self, to_token, doc):
        """Get all tokens that belong to an infinitive phrase starting with 'to'"""
        inf_tokens = {to_token.i}
        
        # If 'to' is followed by a verb, include the verb and its dependents
        if to_token.i + 1 < len(doc):
            next_token = doc[to_token.i + 1]
            if next_token.pos_ == 'VERB' and next_token.tag_ == 'VB':
                # Add the main verb
                inf_tokens.add(next_token.i)
                
                # Add verb's direct objects and complements
                for child in next_token.children:
                    if child.dep_ in ['dobj', 'pobj', 'advmod', 'prep']:
                        inf_tokens.add(child.i)
                        # For prepositional objects, include the whole prepositional phrase
                        if child.dep_ == 'prep':
                            for grandchild in child.children:
                                if grandchild.dep_ == 'pobj':
                                    inf_tokens.add(grandchild.i)
        
        # Alternative: if 'to' is aux to a verb head
        elif to_token.dep_ == 'aux' and to_token.head.pos_ == 'VERB':
            verb = to_token.head
            inf_tokens.add(verb.i)
            
            # Add the verb's complements that are part of the infinitive
            for child in verb.children:
                if child.dep_ in ['dobj', 'pobj', 'advmod']:
                    inf_tokens.add(child.i)
        
        return inf_tokens
    
    def _classify_remaining_token(self, token, doc):
        """Classify tokens that don't belong to major phrase types"""
        
        # Time/place nouns acting as adverbs
        if (token.pos_ == 'NOUN' and 
            token.dep_ in ['npadvmod', 'tmod'] and
            token.text.lower() in ['today', 'tomorrow', 'yesterday', 'now', 'then']):
            return 'ADVP'
        
        # Determiners are often part of noun phrases, but if not already marked
        if token.pos_ == 'DET':
            return 'DP'  # Determiner Phrase
        
        # Coordinating conjunctions
        if token.pos_ == 'CCONJ':
            return 'CONJP'
        
        # Subordinating conjunctions and complementizers
        if token.pos_ == 'SCONJ' or token.dep_ == 'mark':
            return 'CONJP'
        
        # Particles and other function words
        if token.pos_ in ['PART', 'INTJ']:
            return 'PART'
        
        # Punctuation (should not be classified as phrase type)
        if token.pos_ == 'PUNCT':
            return 'O'
        
        # Numbers
        if token.pos_ == 'NUM':
            return 'NUM'
        
        # Pronouns not in noun chunks
        if token.pos_ == 'PRON':
            return 'NP'  # Treat standalone pronouns as noun phrases
        
        # Default for anything else
        return 'O'
    
    def find_common_patterns(self, token_sequences):
        """Find all common patterns across sequences"""
        if len(token_sequences) < 2:
            print("Need at least 2 texts to find common patterns")
            return []
        
        # Find all patterns
        patterns = defaultdict(lambda: {'count': 0, 'files': set()})
        
        # Use the shortest sequence as base
        base_idx = min(range(len(token_sequences)), key=lambda i: len(token_sequences[i][1]))
        base_file, base_seq = token_sequences[base_idx]
        
        # Try all possible substrings from the base sequence
        n = len(base_seq)
        for length in range(n, 0, -1):
            for start in range(n - length + 1):
                pattern = tuple(base_seq[start:start + length])
                
                # Check if this pattern exists in all other sequences
                found_in_all = True
                total_count = 0
                files_with_pattern = set()
                
                for file_path, seq in token_sequences:
                    count = self.count_pattern_in_sequence(pattern, seq)
                    if count > 0:
                        total_count += count
                        files_with_pattern.add(file_path)
                    else:
                        found_in_all = False
                
                # Only include patterns found in at least 2 files
                if len(files_with_pattern) >= 2:
                    patterns[pattern]['count'] = total_count
                    patterns[pattern]['files'] = files_with_pattern
        
        # Convert to list and sort by length (longest first), then by count
        result = []
        for pattern, info in patterns.items():
            result.append((pattern, info['count'], len(info['files'])))
        
        result.sort(key=lambda x: (len(x[0]), x[1], x[2]), reverse=True)
        return result
    
    def count_pattern_in_sequence(self, pattern, sequence):
        """Count occurrences of pattern in sequence"""
        count = 0
        pattern_len = len(pattern)
        seq_len = len(sequence)
        
        for i in range(seq_len - pattern_len + 1):
            if tuple(sequence[i:i + pattern_len]) == pattern:
                count += 1
        
        return count
    
    def format_pattern(self, pattern):
        """Format pattern for display"""
        if self.level == 1:
            return ' '.join(pattern)
        elif self.level == 2:
            return ' '.join([f"{token}({pos})" for token, pos in pattern])
        elif self.level == 3:
            return ' '.join([f"{token}[{phrase}]" for token, phrase in pattern])
        elif self.level == 4:
            return ' '.join([f"{token}({pos})[{phrase}]" for token, pos, phrase in pattern])
    
    def analyze_texts(self, texts_list):
        """Analyze texts from list of strings for web API"""
        if len(texts_list) < 2:
            return {
                "error": "Need at least 2 texts to find common patterns",
                "patterns": []
            }
        
        try:
            # Tokenize each text
            token_sequences = []
            for i, text in enumerate(texts_list):
                if text and text.strip():
                    tokens = self.tokenize(text.strip())
                    if tokens:
                        token_sequences.append((f"Text {i+1}", tokens))
            
            if len(token_sequences) < 2:
                return {
                    "error": "Need at least 2 non-empty texts to find patterns",
                    "patterns": []
                }
            
            # Find common patterns
            patterns = self.find_common_patterns(token_sequences)
            
            # Format results for JSON response
            result_patterns = []
            max_display = min(20, len(patterns))
            
            for pattern, count, num_files in patterns[:max_display]:
                formatted = self.format_pattern(pattern)
                result_patterns.append({
                    "pattern": formatted,
                    "length": len(pattern),
                    "count": count,
                    "texts": num_files
                })
            
            return {
                "success": True,
                "num_texts": len(token_sequences),
                "level": self.level,
                "total_patterns": len(patterns),
                "patterns": result_patterns
            }
            
        except Exception as e:
            return {
                "error": f"Analysis failed: {str(e)}",
                "patterns": []
            }
    
    def run(self, folder_path):
        """Main execution for command line"""
        # Get files
        files = self.get_files_from_folder(folder_path)
        print(f"Found {len(files)} text file(s) in {folder_path}")
        
        # Read and tokenize texts
        texts = self.read_texts(files)
        if len(texts) < 2:
            print("Need at least 2 texts with content to find patterns")
            return
        
        print(f"Processing {len(texts)} text(s)...")
        
        # Tokenize each text
        token_sequences = []
        for file_path, text in texts:
            tokens = self.tokenize(text)
            if tokens:
                token_sequences.append((file_path, tokens))
                print(f"  - {os.path.basename(file_path)}: {len(tokens)} tokens")
        
        # Find common patterns
        print(f"\nFinding common patterns (Level {self.level})...")
        patterns = self.find_common_patterns(token_sequences)
        
        # Display results
        print(f"\nFound {len(patterns)} common patterns:\n")
        
        if not patterns:
            print("No common patterns found.")
            return
        
        # Show top patterns
        max_display = min(20, len(patterns))
        for i, (pattern, count, num_files) in enumerate(patterns[:max_display], 1):
            formatted = self.format_pattern(pattern)
            print(f"{i}. Pattern: \"{formatted}\"")
            print(f"   Length: {len(pattern)} tokens")
            print(f"   Total occurrences: {count}")
            print(f"   Found in {num_files} file(s)")
            print()
        
        if len(patterns) > max_display:
            print(f"... and {len(patterns) - max_display} more patterns")


def main():
    parser = argparse.ArgumentParser(description='Find longest shared patterns in text files')
    parser.add_argument('folder', help='Folder containing text files')
    parser.add_argument('--level', type=int, default=1, choices=[1, 2, 3, 4],
                        help='Analysis level: 1=token, 2=token+POS, 3=token+phrase, 4=token+POS+phrase')
    
    args = parser.parse_args()
    
    # Create pattern finder
    finder = PatternFinder(level=args.level)
    
    # Run analysis
    finder.run(args.folder)


if __name__ == '__main__':
    main()