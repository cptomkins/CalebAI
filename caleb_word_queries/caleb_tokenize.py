import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Download NLTK resources (run this once if you haven't already)
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# These are okay to be between a verb and an object
OK_PRE_OBJECT = [ 'IN', # Preposition
                  'DT', # Determiner ex: 'a' 'the' 'our'
                  'JJ', # Adjective
                  ]

QUESTION_PREFIXES = ['WP', 'WDT', 'WRB', 'VB', 'MD', 'TO']


def caleb_tokenize(sentence, debug=False):
    # Tokenize the sentence
    tokens = word_tokenize(sentence)
    
    # Get part-of-speech tags for each token
    pos_tags = pos_tag(tokens)
    if debug:
        print("pos_tags", pos_tags)
    
    return tokens, pos_tags

def find_verb(sentence):
    
    tokens, pos_tags = caleb_tokenize(sentence)
    
    # Find the verb
    verbs = [token for token, pos in pos_tags if pos.startswith('VB')]
    if not verbs:
        return None
    verb = verbs[0]
    
    return verb

def find_object(sentence, debug=False):
    
    tokens, pos_tags = caleb_tokenize(sentence, debug=debug)
    
    verb = find_verb(sentence)
    if debug:
        print('finding object for verb', verb)
    if not verb:
        return None
    
    # Find the index of the verb
    verb_index = tokens.index(verb)
    
    # Search for nouns or noun phrases after the verb
    object_tokens = []
    for token, pos in pos_tags[verb_index+1:]:
        if pos.startswith('NN') or pos.startswith('PRP'):  # Noun or Pronoun
            object_tokens.append(token)
        elif pos in OK_PRE_OBJECT:
            continue
        else:
            break
    
    if object_tokens:
        return ' '.join(object_tokens)
    
def find_question(sentence, debug=False):
    tokens, pos_tags = caleb_tokenize(sentence, debug=debug)
    questions = [(token, pos) for token, pos in pos_tags
                if any(pos.startswith(prefix)
                       for prefix in QUESTION_PREFIXES)]
    selected_question = None
    
    for question in questions:
        if not question[1].startswith('WP'):
            continue
        selected_question = question
        break
    
    if selected_question:
        return selected_question[0]
    
    if debug:
        print('ERROR: Only WP questions are supported for now.')
    

if __name__=='__main__':
    # Example sentence
    sentence = 'How old is he?'
    print('find question', find_question(sentence, debug=True))
    print('find_object', find_object(sentence))
