FROM pasmod/miniconder2

WORKDIR /var/www
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .
RUN py.test --pep8

