from snownlp import SnowNLP
#from harvesttext import HarvestText
from trial3 import *
import time
from progressbar import *

def divide_words(data):
    s=SnowNLP(data)
    output= my_model_passage(s.sentences)
    return output

'''
def divide_words(data):
    s=SnowNLP(data)
    output='' 
    widgets = ['Progress: ',Percentage(), ' ', Bar('#'),' ', Timer(),
           ' ', ETA(), ' ', FileTransferSpeed()]
    progress = ProgressBar(widgets=widgets)

    for j in progress(range(len(s.sentences))):
        sentence=s.sentences[j]
        s2=SnowNLP(sentence)
        for word in s2.words:
            ht=HarvestText()
            tag=ht.named_entity_recognition(word)       
            for key in tag:
                if tag[key]=='机构名':
                    for i in range(len(word)):
                        if i==0:
                            output=output+word[i]+" B-ORG\n"
                        elif i==len(word)-1:
                            output=output+word[i]+" E-ORG\n"
                        else:
                            output=output+word[i]+" M-ORG\n"
                elif tag[key]=='人名':
                    for i in range(len(word)):
                        if i==0:
                            output=output+word[i]+" B-PER\n"
                        elif i==len(word)-1:
                            output=output+word[i]+" E-PER\n"
                        else:
                            output=output+word[i]+" M-PER\n"
                elif tag[key]=='地名':
                    for i in range(len(word)):
                        if i==0:
                            output=output+word[i]+" B-LOC\n"
                        elif i==len(word)-1:
                            output=output+word[i]+" E-LOC\n"
                        else:
                            output=output+word[i]+" M-LOC\n"
            if tag=={}:
                for i in range(len(word)):
                    output=output+word[i]+" O\n"

        output=output+"\n"

    return output
'''
