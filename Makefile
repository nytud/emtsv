
# raw text input
RAWINPUT=test_input/input.test
#RAWINPUT=test_input/puzser.test
#
# some larger raw testfiles available on juniper...
#RAWINPUT=/store/projects/e-magyar/test_input/hundredthousandwords.txt

# input crafted directly for emTag
#TAGINPUT=test_input/emTag.test

# input crafted directly for emDep
#DEPINPUT=test_input/emDep.test

# ----------

all: usage

# always update according to targets below :)
usage:
	@echo
	@echo "You can..."
	@echo " make test-tok-morph"
	@echo " make test-tok-morph-tag"
	@echo " make test-tok-morph-tag-single"
	@echo " make test-tok-dep-single"
	@echo " make test-tok-chunk-ner-single"
	@echo " make test-tok-cons-single"
#	@echo " make test-tag"
#	@echo " make test-dep"
	@echo

# ----------

# testing emTok + emMorph (separately)
test-tok-morph:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok \
     | python3 ./emtsv.py morph

# testing emTok + emMorph + emTag (separately)
test-tok-morph-tag:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok \
     | python3 ./emtsv.py morph \
     | python3 ./emtsv.py pos

# testing emTok + emMorph + emTag
test-tok-morph-tag-single:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok,morph,pos

# testing emTok + emMorph + emTag + em_morph2UD + emDepUD
test-tok-dep-single:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok,morph,pos,conv-morph,dep

# testing emTok + emMorph + emTag + em_morph2UD + emDepUD + emChunk + emNer
# XXX currently without emCons
test-all-single:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok,morph,pos,conv-morph,dep,chunk,ner

# ----------

# testing emTok + emMorph + emTag + em_morph2UD + emDepUD + emCons
test-tok-cons-single:
	@cat $(RAWINPUT) \
     | python3 ./emtsv.py tok,morph,pos,conv-morph,dep,cons

# ----------

update_repo:
	@if [ "$$(git status --porcelain)" ] ; then \
		echo 'Working dir is dirty!' ; \
		exit 1 ; \
		fi
	@git submodule foreach git pull origin master && git pull
.PHONY: update_repo


# testing emTag only -- ezt majd!
#test-tag:
#	@cat $(TAGINPUT) \
#    | python3 ./emtsv.py pos

#	testing emDep only -- ezt majd!
#test-dep:
#	@cat $(DEPINPUT) \
#    | python3 ./emtsv.py dep


# ----------------------
# Docker related targets
# ----------------------

## build docker image
dbuild:
	docker build -t emtsv:latest .
.PHONY: dbuild


## run docker container in background, without volume mapping
drun:
	@ if [ -f docker/id.txt ] ; then make -s dstop ; fi
	@myport=$$(./docker/freeportfinder.sh) ; \
		if [ -z "$${myport}" ] ; then echo 'ERROR: no free port' ; exit 1 ; fi ; \
		docker run -p $${myport}:5000 --rm -d emtsv:latest >docker/id.txt ; \
		echo "OK: emtsv container run on port $${myport}" ;
.PHONY: drun


# connect container that is already running
dconnect:
	@if [ -z "$(NAME)" ] ; then \
		echo 'usage: make dconnect NAME=container_name' ; \
		exit 1 ; fi
	@echo "connect to container: $(NAME)"
	@docker exec -it $(NAME) /bin/sh
.PHONY: dconnect

## enter into the container
dshell:
	@ if [ -f docker/id.txt ] ; then make -s dstop ; fi
	@docker run -p 5000:5000 --rm -it emtsv:latest sh
.PHONY: dshell


## stop running docker container, based on container ID in id.txt file
dstop: docker/id.txt
	@docker container stop $$(cat docker/id.txt) || \
		echo "WARNING: container not found: $$(cat docker/id.txt)"
	@rm docker/id.txt
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
