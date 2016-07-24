# Simurg

A tool to create extendable multilingual corpora for abstractive text summarization (and other applications).
## Motivation
Abstractive single document summarization is considered as a difficult problem in the field of artificial intelligence and natural language processing. Meanwhile and specifically in the last two years, several deep learning summarization approaches were introduced that once again attracted the attention of researchers to this field.

It is a known issue that deep learning approaches do not work well with small amount of data. With some exceptions, this is unfortunately the case for most of the data sets available for the summarization task. Beside this problem, it should be considered that phonetic, morphological, semantic and syntactic features of the language are constantly changing over time and unfortunately most of the summarization corpora are constructed from old resources. Another problem is the language of the corpora. Not only in the summarization field, but also in other fields of natural language processing, most of the corpora are only available in English. In addition to the above problems, licence terms and fees of the corpora is a obstacle that prevent many academics and specifically non-academics from accessing these data.

Simurg is an open source framework to create an extensable multilingual corpus for abstractive single document summarization that addresses the above mentioned problems.

## Architecture
Creating the corpus consists of two phases:
- Constructing the template corpus
![Image of Yaktocat](http://github.com/pasmod/simurg/images/architecture.jpg)

- Populating the template corpus
