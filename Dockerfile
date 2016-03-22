FROM pasmod/miniconder2

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran

WORKDIR /var/www
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .
RUN py.test --pep8

