import nltk

class PronounResolver:
    noun_scores = {}  # Dictionary to store noun scores and genders

    def update_noun_scores_after_sentence(self):
        for noun in self.noun_scores:
            self.noun_scores[noun]['score'] *= 0.5  # Halve the noun's score after every sentence

    def resolve_pronouns(self, text):
        # Tokenize the text into sentences
        sentences = nltk.sent_tokenize(text)
        resolved_text = []
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)  # Tokenize the sentence into words
            tagged_words = nltk.pos_tag(words)  # Perform part-of-speech tagging
            resolved_sentence = []
            nouns_in_sentence = set()  # Track nouns in the current sentence

            for word, pos in tagged_words:
                if pos in ['NN', 'NNS', 'NNP', 'NNPS']:  # Check if the word is a noun
                    noun = word.lower()
                    if noun in self.noun_scores:
                        self.noun_scores[noun]['score'] += 1  # Increment noun score for every occurrence
                    else:
                        # Assign an initial score of 1 and default gender (e.g., 'unknown') to the noun
                        self.noun_scores[noun] = {'score': 1, 'gender': 'unknown'}
                    resolved_sentence.append(word)  # Keep the noun in the resolved sentence
                    nouns_in_sentence.add(noun)  # Add the noun to the set
                elif word.lower() in ['he', 'him', 'his', 'she', 'her']:
                    # Choose the noun with the highest score and matching gender as the antecedent for the pronoun
                    antecedent = max(
                        (noun for noun in self.noun_scores if noun not in nouns_in_sentence and 
                         self.noun_scores[noun]['gender'] == word.lower()),
                        key=lambda x: self.noun_scores[x]['score'],
                        default=None
                    )
                    if antecedent:
                        resolved_sentence.append(antecedent)  # Resolve the pronoun to the noun
                    else:
                        resolved_sentence.append(word)  # If no suitable antecedent, keep the pronoun
                else:
                    resolved_sentence.append(word)

            resolved_text.append(' '.join(resolved_sentence))
            self.update_noun_scores_after_sentence()  # Halve noun scores after each sentence

        print(self.noun_scores)
        return resolved_text

# Example text with gender-specific nouns
text = "John went to the store. He bought a book. Mary saw him there. She smiled at him."

# Assign gender information to nouns
resolver = PronounResolver()
resolver.noun_scores['john'] = {'score': 0, 'gender': 'male'}
resolver.noun_scores['store'] = {'score': 0, 'gender': 'neutral'}
resolver.noun_scores['book'] = {'score': 0, 'gender': 'neutral'}
resolver.noun_scores['mary'] = {'score': 0, 'gender': 'female'}

resolved_text = resolver.resolve_pronouns(text)
for sentence in resolved_text:
   print(sentence)
