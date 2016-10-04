# Simurg

[![Build Status](https://travis-ci.org/pasmod/simurg.svg?branch=master)](https://travis-ci.org/pasmod/simurg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/fchollet/keras/blob/master/LICENSE)

A tool to create extendable multilingual corpora for abstractive text summarization (and other applications).
## Motivation
Abstractive single document summarization is considered as a difficult problem in the field of artificial intelligence and natural language processing. Meanwhile and specifically in the last two years, several deep learning summarization approaches were introduced that once again attracted the attention of researchers to this field.

It is a known issue that deep learning approaches do not work well with small amount of data. With some exceptions, this is unfortunately the case for most of the data sets available for the summarization task. Beside this problem, it should be considered that phonetic, morphological, semantic and syntactic features of the language are constantly changing over time and unfortunately most of the summarization corpora are constructed from old resources. Another problem is the language of the corpora. Not only in the summarization field, but also in other fields of natural language processing, most of the corpora are only available in English. In addition to the above problems, licence terms and fees of the corpora is a obstacle that prevent many academics and specifically non-academics from accessing these data.

Simurg is an open source framework to create an extensable multilingual corpus for abstractive single document summarization that addresses the above mentioned problems.

## Architecture
Creating the corpus consists of two phases:
- Constructing the template corpus: The template corpus is the sharable part of the Simurg corpus.

<img src="https://github.com/pasmod/simurg/blob/master/images/architecture.jpg" width="300", align="middle">
- Populating the template corpus: In this phase the template corpus will be populated with all the required information and the result will be a collection of JSON documents.

## Dependencies
- [Docker](https://www.docker.com/)

## Setup the Project
- ```make build```: to build the docker image
- ```make start_redis```: to start the redis server
- ```make connect_redis```: to use the redis command line interface
- ```make run```: to run the container

## Template Corpus
To create the template corpus use the following commands:

```make run```: to run the container

In the container run ```python``` and then enter the following two python commands:

```python
import simurg
simurg.create_template_corpus(lang='de')
```

## Populating the Template Corpus
Run the following command to create the final corpus:

```make run```: to run the container

In the container run ```python``` and then enter the following two python commands:
```python
import simurg
simurg.populate_template_corpus(lang='de')
```

## Adding New Languages:
Currently English, German, French and Italian are supported. Adding a new language is simple:
In the file ```config.py``` modify the variable ```REDIS_DBS``` and add the new language code. Example to add Farsi:
```python
REDIS_DB = {
    'de': 0,
    'en': 1,
    'fr': 2,
    'it': 3,
    'tr': 4
}
```

## Parallel Execution
If you want to construct a corpur for multiple languages at the same time, simply start several containers at the same time. For example to construct English, German, French and Italian corpus at the same time run the following commands:
```bash
make run # For the first language
docker exec -it simurg bash -l # For the second language
docker exec -it simurg bash -l # For the third language
docker exec -it simurg bash -l # For the fourth language
```
