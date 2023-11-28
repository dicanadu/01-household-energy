  # FROM python:3.10.6-buster

  # COPY taxifare /taxifare
  # COPY requirements.txt /requirements.txt

  # RUN pip install --upgrade pip
  # RUN pip install -r requirements.txt

  # CMD uvicorn taxifare.api.fast:app --host 0.0.0.0

  FROM python:3.10.6-buster

  WORKDIR /prod

  # First, pip install dependencies
  RUN pip install --upgrade pip
  COPY ./requirements.txt /prod/requirements.txt
  RUN pip install -r requirements.txt

  # Then only, install api!
  COPY household_predictions household_predictions
  COPY ./setup.py /prod/setup.py
  RUN pip install .

  # COPY Makefile Makefile
  # RUN make reset_local_files

  CMD uvicorn household_predictions.api.fast:app --host 0.0.0.0 --port $PORT


#####
# TOP FIELD

# STATE CODE
# HOUSE TYPE (APARTMENT)

##
#####
