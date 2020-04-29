# Se utiliza de base imagen de python con python 3.6
FROM ubuntu:18.04
# Agregamos los requerimientos a la imagen
ADD requirements.txt /app/requirements.txt

# update repos
RUN apt-get update -y && apt-get upgrade -y

# instalar deps
RUN apt-get install -y build-essential libpq-dev \
	python3-dev libffi-dev python3-pip wget \
	pkg-config libpng-dev

RUN apt-get install -y gdal-bin libgdal-dev
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN pip3 install --upgrade setuptools
RUN pip3 install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"

WORKDIR /app/

# Instalar dependencias de python
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN export LC_ALL=es_ES.UTF-8
# Crear usuario sin privilegios
RUN adduser --disabled-password --gecos '' app
RUN chown -R app:app /app && chmod -R 755 /app
RUN chown -R app:app /usr/local/lib/python3.6/ && chmod -R 755 /usr/local/lib/python3.6/

ENV HOME /home/app
USER app

