from gensim import corpora, models, similarities

documents = ["Human machine interface for lab abc computer applications",
		"A survey of user opinion of computer system response time",
		"The EPS user interface management system",
		"System and human system engineering testing of EPS",
		"Relation of user perceived response time to error measurement",
		"The generation of random binary unordered trees",
		"The intersection graph of paths in trees",
		"Graph minors IV Widths of trees and well quasi ordering",
		"Graph minors A survey"]

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
		for document in documents]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
		for text in texts]

print texts

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict') # store the dictionary, for future reference
print dictionary

print dictionary.token2id

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
print corpus

# To follow Deerwester’s example, we first use this tiny corpus to define a 2-dimensional LSI space:
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)


doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print vec_lsi
