mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

# For REST API modules should be separated by '/'. For simplicity they are replaced in the following script
PYTHON_REST_QUERY := "import sys; \
import requests; \
modules = sys.argv[1].replace(',', '/'); \
r = requests.post(f'http://127.0.0.1:5000/{modules}', files={'file': open(sys.argv[2], encoding='UTF-8')}); \
print(r.text, end='')"

# ----------

all: usage

# always update according to targets below :)
usage:
	@echo
	@echo "You can..."
	@echo " make test-modules RAWINPUT='file.txt' MODULES='tok,morph,etc.'"
	@echo " make test-rest-modules RAWINPUT='file.txt' MODULES='tok,morph,etc.'"
	@echo
.PHONY: usage

# ----------

test-modules:
	@cat $(RAWINPUT) \
     | python3 $(mkfile_dir)/main.py $(MODULES)
.PHONY: test-modules


test-rest-modules:
	@python3 -c ${PYTHON_REST_QUERY} $(MODULES) $(RAWINPUT)
.PHONY: test-rest-modules


test-runnable-docker-modules:
	@cat $(RAWINPUT) \
	 | docker run -i --rm mtaril/emtsv:test $(MODULES)

# ----------

update_repo:
	@if [ "$$(git status --porcelain)" ] ; then \
		echo 'Working dir is dirty!' ; \
		exit 1 ; \
		fi
	@git pull && git submodule foreach git pull origin master
.PHONY: update_repo


venv:
	@if [ -d venv/ ] ; then \
		echo 'Upgrade requirements.' ;\
	else \
		echo 'Create venv/, install requirements.' ;\
		python3 -m venv venv ;\
	fi
	venv/bin/pip install --upgrade cython
	venv/bin/pip install -r requirements.txt
	for req in */requirements.txt ; do venv/bin/pip install -r $${req} ; done
.PHONY: venv

# ----------------------
# Docker related targets
# ----------------------

VERSION = $$(grep -E "__version__\s*=\s*'[^']+'" __init__.py | sed  -r "s/__version__ = '([^']+)'/\1/")

## build docker image
dbuild:
	docker build -t mtaril/emtsv:latest -t mtaril/emtsv:$(VERSION) .
.PHONY: dbuild


## build docker test image
dbuildtest:
	docker build -t mtaril/emtsv:test .
.PHONY: dbuildtest


## run docker container in background, without volume mapping
drun:
	@make -s dstop
	@myport=$$(./docker/freeportfinder.sh) ; \
		if [ -z "$${myport}" ] ; then echo 'ERROR: no free port' ; exit 1 ; fi ; \
		docker run --name emtsv -p $${myport}:5000 --rm -d mtaril/emtsv:latest ; \
		echo "OK: emtsv container run on port $${myport}" ;
.PHONY: drun


# connect emtsv container that is already running
dconnect:
	@if [ "$$(docker container ls -f name=emtsv -q)" ] ; then \
		docker exec -it emtsv /bin/sh ; \
	else \
		echo 'no running emtsv container' ; \
	fi
.PHONY: dconnect


# test the test image
dtest: # dbuildtest
	@./test/dtest.sh
.PHONY: dtest



## stop running emtsv container
dstop:
	@if [ "$$(docker container ls -f name=emtsv -q)" ] ; then \
		docker container stop emtsv ; \
	else \
		echo 'no running emtsv container' ; \
	fi
.PHONY: dstop


## show images and containers
dls:
	@echo 'IMAGES:'
	@docker image ls
	@echo
	@echo 'CONTAINERS:'
	@docker container ls
.PHONY: dls


## delete unnecessary containers and images
dclean:
	@docker container prune -f
	@docker image prune -f
.PHONY: dclean
