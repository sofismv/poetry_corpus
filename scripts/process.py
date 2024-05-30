import stanza
stanza.download('ru')
import json
import string 
from collections import defaultdict
from tqdm import tqdm
import re
from rusenttokenize import ru_sent_tokenize

def preprocess(poems):
    ''' 
    delete spaces, split into sentences manually
    '''
    for poem_id, poem in enumerate(poems):
        sentences = ru_sent_tokenize(poem['poem'])
        poem_text = [re.sub(r'\r\n', ' ', sentence).lower() for sentence in sentences]
        poem_text = '\n\n'.join(poem_text)
        poems[poem_id]['poem'] = poem_text
    return poems

def process(poems):
    ''' 
    tokenization, lemmatization, index 
    '''    
    poems = preprocess(poems)
    nlp = stanza.Pipeline('ru', processors='tokenize,pos,lemma,depparse', tokenize_no_ssplit = True)
    index = defaultdict(list)
    for poem_id, poem in tqdm(enumerate(poems)):
        doc = nlp(poem['poem'])
        sentences = []
        for sen_id, dsentence in enumerate(doc.sentences):
            sentence = []
            for word in dsentence.words:
                # add to index if not punctuation
                if word.upos != "PUNCT":
                    index[word.lemma].append((poem_id, sen_id, word.id))
                token =  {
                        'word': word.text,
                        'lemma': word.lemma,
                        'speech_part': word.upos,
                        'id': word.id,
                        'head': word.head,
                        'deprel': word.deprel,
                        'feats': word.feats
                        }
                sentence.append(token)
            sentences.append(sentence)
        poems[poem_id]['sentences'] = sentences
    return poems, index

with open('poems.json', 'r') as file:
    poems = json.JSONDecoder().decode(file.read())

corpus, index = process(poems)

with open("corpus.json", 'w') as file:
    json.dump(corpus, file)

with open("index.json", 'w') as file:
    json.dump(index, file)