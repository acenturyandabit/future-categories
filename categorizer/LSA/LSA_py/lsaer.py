#import modules
import os.path
from gensim import corpora
from gensim.models import LsiModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models.coherencemodel import CoherenceModel
from multiprocessing import freeze_support
import matplotlib.pyplot as plt
import json
import csv
import re

def load_data(path,file_name):
    """
    Input  : path and file_name
    Purpose: loading text file
    Output : list of paragraphs/documents and
             title(initial 100 words considred as title of document)
    """
    documents_list = []
    titles=[]
    with open( os.path.join(path, file_name) ,"r") as fin:
        for line in fin.readlines():
            text = line.strip()
            documents_list.append(text)
            #titles.append( text[0:min(len(text),100)] )
    print("Total Number of Documents:",len(documents_list))
    return documents_list,documents_list

def load_json(path,file_name):
    """
    Input  : path and file_name
    Purpose: loading text file
    Output : list of paragraphs/documents and
             title(initial 100 words considred as title of document)
    """
    documents_list = []
    titles=[]
    with open( os.path.join(path, file_name) ,"r") as fin:
        lines=fin.readlines()
        rawData=json.loads(lines[0])
        documents_list=[i['text'] for i in rawData]
        titles=( text[0:min(len(text),100)] for text in documents_list)
    print("Total Number of Documents:",len(documents_list))
    return documents_list,titles

def preprocess_data(doc_set,custom_stops=[]):
    """
    Input  : docuemnt list
    Purpose: preprocess text (tokenize, removing stopwords, and stemming)
    Output : preprocessed text
    """
    # initialize regex tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    # create English stop words list
    en_stop = set(stopwords.words('english'))
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    # list for tokenized documents in loop
    texts = []
    # loop through document list
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        # custom stops
        custom_stopped_tokens = [i for i in stemmed_tokens if not i in custom_stops]
        # add tokens to list
        texts.append(custom_stopped_tokens)
    return texts

def prepare_corpus(doc_clean):
    """
    Input  : clean document
    Purpose: create term dictionary of our courpus and Converting list of documents (corpus) into Document Term Matrix
    Output : term dictionary and Document Term Matrix
    """
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. dictionary = corpora.Dictionary(doc_clean)
    dictionary = corpora.Dictionary(doc_clean)
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # generate Lsi model
    return dictionary,doc_term_matrix

def create_gensim_lsa_model(doc_clean,number_of_topics,words):
    """
    Input  : clean document, number of topics and number of words associated with each topic
    Purpose: create LSA model using gensim
    Output : return LSA model
    """
    dictionary,doc_term_matrix=prepare_corpus(doc_clean)
    # generate LSA model
    lsamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary)  # train model
    print(lsamodel.print_topics(num_topics=number_of_topics, num_words=words))
    return lsamodel

def compute_coherence_values(dictionary, doc_term_matrix, doc_clean, stop, start=2, step=3):
    """
    Input   : dictionary : Gensim dictionary
              corpus : Gensim corpus
              texts : List of input texts
              stop : Max num of topics
    purpose : Compute c_v coherence for various number of topics
    Output  : model_list : List of LSA topic models
              coherence_values : Coherence values corresponding to the Lsi model with respective number of topics
    """
    coherence_values = []
    for number_of_topics in range(start, stop, step):
        # generate LSA model
        print (number_of_topics)
        model = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary)  # train model
        print(number_of_topics)
        coherencemodel = CoherenceModel(model=model, texts=doc_clean, dictionary=dictionary, coherence='u_mass')
        print(number_of_topics)
        coherence_values.append(coherencemodel.get_coherence())
        print(number_of_topics)
        del model
    return coherence_values

def plot_graph(doc_clean,start, stop, step):
    dictionary,doc_term_matrix=prepare_corpus(doc_clean)
    coherence_values = compute_coherence_values(dictionary, doc_term_matrix,doc_clean,
                                                            stop, start, step)
    # Show graph
    x = range(start, stop, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    print("got here")
    plt.show()

if not __name__ == "__main__":
    exit()
opmode="full"

#custom_stop = set(["new","â","use","system","year","time","mani","world","first","countri","also","would","includ","000","decad","number","howev","power","increas","human","major","develop"])
custom_stop=set(["â"])
document_list,titles=load_json("","clean-axios.json")
clean_text=preprocess_data(document_list,custom_stop)

# graph plot first to determine what value we should use for number_of_topics
if opmode=="graph":
    freeze_support()
    start,stop,step=2,20,1
    plot_graph(clean_text,start,stop,step)
    exit()

# LSA Model
number_of_topics=13
words=10
model=create_gensim_lsa_model(clean_text,number_of_topics,words)

# Query the model: returns an array showing which topic this dictionary fits into.
dictionary,doc_term_matrix=prepare_corpus(clean_text)
corpus_topics=list(model[doc_term_matrix])
corpus_topics=[[i[1] for i in a] for a in corpus_topics]
for t,i in enumerate(corpus_topics):
    i.append(document_list[t])

f=open("output.csv","w", newline='')
csvwriter=csv.writer(f)
print(corpus_topics[1])
csvwriter.writerows(corpus_topics)

#print(corpus_topics)
print("\n\n\n\n")

# Identify words that need to be added to the custom stop list in the next run
# by taking all words in the topic and picking out the most common ones.
topic_representation = model.print_topics(num_topics=number_of_topics, num_words=words)
topic_representation=[i[1] for i in topic_representation]
pattern=re.compile('"(.+?)"')
topic_words=[pattern.findall(topic) for topic in topic_representation]
print(topic_words)
word_count={}
for t in topic_words:
    for i in t: 
        if not i in word_count:
            word_count[i]=0
        word_count[i]+=1

dictlist=list(word_count.items())
dictlist.sort(key=lambda i: i[1])
print(dictlist)
