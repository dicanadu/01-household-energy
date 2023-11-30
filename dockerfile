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
  COPY ./requirements_prod.txt /prod/requirements.txt
  RUN pip install -r requirements.txt

  # Install our packages (for some reason they are two now)
  COPY household_predictions household_predictions
  COPY household_package household_package
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
