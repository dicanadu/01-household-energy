FROM python:3.10.6-buster

  # First, pip install dependencies
COPY requirements.txt requirements.txt
COPY api api
COPY household_package household_package
COPY setup.py setup.py
COPY model_h5 model_h5


RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install .

  # COPY Makefile Makefile
  # RUN make reset_local_files

CMD uvicorn api.app:app --host 0.0.0.0 --port $PORT


#####
# TOP FIELD

# STATE CODE
# HOUSE TYPE (APARTMENT)

##
#####
