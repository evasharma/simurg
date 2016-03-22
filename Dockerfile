FROM pasmod/miniconder2

RUN apt-get update
RUN apt-get -y build-essential
RUN apt-get install -y python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev 

WORKDIR /var/www
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .
RUN py.test --pep8

