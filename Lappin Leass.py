import nltk

class PronounResolver:
    noun_scores = {}  # Dictionary to store noun scores

    def update_noun_scores_after_sentence(self):
        for noun in self.noun_scores:
            self.noun_scores[noun] *= 0.5  # Halve the noun's score after every sentence

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
                        self.noun_scores[noun] += 1  # Increment noun score for every occurrence
                    else:
                        self.noun_scores[noun] = 1  # Assign an initial score of 1 to the noun
                    resolved_sentence.append(word)  # Keep the noun in the resolved sentence
                    nouns_in_sentence.add(noun)  # Add the noun to the set
                elif word.lower() in ['he', 'him', 'his', 'she', 'her']:
                    # Choose the noun with the highest score that is not in the current sentence
                    antecedent = max(
                        (noun for noun in self.noun_scores if noun not in nouns_in_sentence),
                        key=self.noun_scores.get,
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

# Example text
text = "John went to the store. He bought a book. Mary saw him there. She smiled at him."

resolver = PronounResolver()
resolved_text = resolver.resolve_pronouns(text)
for sentence in resolved_text:
    print(sentence)
