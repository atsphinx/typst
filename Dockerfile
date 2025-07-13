FROM sphinxdoc/sphinx-latexpdf

WORKDIR /docs
ADD . /docs
RUN pip3 install --group=docs .
