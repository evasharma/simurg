FROM pasmod/miniconder2

RUN apt-get update && \
	apt-get install -y build-essential libxml2-dev libxslt-dev libsm6 libxrender1 libfontconfig1 libicu-dev python-dev libhunspell-dev && \
	apt-get clean

RUN conda install -y \
  beautifulsoup4==4.4.1

RUN pip install redis
RUN pip install unidecode

WORKDIR /var/www
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN py.test --pep8

