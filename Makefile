# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* 01-household-energy/*.py

black:
	@black scripts/* 01-household-energy/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr 01-household-energy-*.dist-info
	@rm -fr 01-household-energy.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

# ----------------------------------
#      		PACKAGE ACTIONS
# ----------------------------------
.DEFAULT_GOAL := default
reinstall_package:
	@pip uninstall -y household_prediction || :
	@pip install -e .

reload_env:
	direnv reload

# ----------------------------------
#      		DOCKER ACTIONS
# ----------------------------------
# .DEFAULT_GOAL := default
build_docker_prod:
	docker build --platform linux/amd64 -t ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/household-predictions/${GAR_IMAGE}:prod

push_to_artifact:
	docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/household-predictions/${GAR_IMAGE}:prod

deploy_cloud_run:
	gcloud run deploy --image ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/household-predictions/${GAR_IMAGE}:prod --memory ${GAR_MEMORY} --region ${GCP_REGION} --env-vars-file .env.yaml

shutdown_cloud_instance:
	gcloud run services delete ${INSTANCE}
