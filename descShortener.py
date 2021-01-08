from __future__ import unicode_literals, print_function
import spacy
import plac
import pandas as pd
from spacy.matcher import Matcher
from spacy import displacy

#training requirements
from spacy.util import minibatch, compounding
import random

TRAIN_DATA = [
    ('We require SQL', {
        'entities': [(10, 12, 'LANGAUGE')]
    }),
    ('2+ years of Javascript experience', {
        'entities': [(12, 22, 'LANGUAGE')]
    }),
    ('4+ years of Python experience', {
        'entities': [(12, 18, 'LANGUAGE')]
    })
]


##Load the NLP model, in this case the english default one
nlp = spacy.load("en_core_web_sm")

##I need to update the NER model to add a language, framework, technology classification

#Get the pipeline for the NER
ner = nlp.get_pipe("ner")
ner.add_label('LANGUAGE')

#resume training
optimizer = nlp.resume_training()
move_names = list(ner.move_names)

#List of the pipes I want to train
pipe_exception = ["ner", "trf_wordpiecer", "trf_tok2vec"]

#List of unaffected pipes
other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exception]


#Do the training here
with nlp.disable_pipes(*other_pipes):

    sizes = compounding(1.0, 4.0, 1.001)

    #train for 30 iterations
    for itn in range(0,30):
        #shuffle the order of the data
        random.shuffle(TRAIN_DATA)
        #batch the examples
        batches = minibatch(TRAIN_DATA, size=sizes)

        #lose stuff
        losses ={}
        for batch in batches:
            texts, annotations = zip(*batch)
            #calling update() over the iteration
            nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
            print("Losses", losses)

desc = pd.read_csv("jobs.csv")
descColumn = desc["Description"]

jobDesc = nlp(descColumn[0])

matcher = Matcher(nlp.vocab)


def preprocessTokenToLowerLemma(token):
    return token.lemma_.strip().lower()

##TO-DO: Add priority list for tokens
def validToken(token):
    #if the token is a stop word or punctuation remove, it is not valid
    if (token.is_stop or token.is_punct):
        return False
    else:
        return True

#Extract a salary
def extractSalary(token):
    
    if token.ent_type_ == 'MONEY':
        return True
    else:
        return False

for ent in jobDesc.ents:
    if ent.label_ == 'LANGUAGE':
        print(ent.text, ent.label_)