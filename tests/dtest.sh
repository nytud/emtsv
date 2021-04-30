#! /bin/bash

echo 'Test "mtaril/emtsv:test" docker image.'

RED="\033[1;31m"
GREEN="\033[1;32m"
NOCOLOR="\033[0m"

TESTDIR=$(mktemp -d /tmp/dtestXXXXXX)
INPUT='test/input/alaptorveny.txt'
GOLD='test/gold/alaptorveny_dep.tsv'
BASENAME=$(basename $INPUT)
MODULES='tok,morph,pos,conv-morph,dep'
OUTPUT=""


function find_free_port {
    # parameters: no
    # return: number of a free port
    res=""
    for port in {10001..15000} ; do
        (echo '' >/dev/tcp/localhost/$port) >/dev/null 2>&1 || { res=$port; break; } ;
    done
    echo "$res"
}


function spin {
    # spinner (aka. lightweight progressbar)
    # source: https://mywiki.wooledge.org/BashFAQ/034
    local i=0
    local sp='/-\|'
    local n=${#sp}
    printf ' '
    sleep 0.1
    while true; do
        >&2 printf '\b%s' "${sp:i++%n:1}"
        sleep 0.5
    done
}


function run_docker {
    # Run (mtaril/emtsv:test) docker image in cli or rest mode.
    # parameters:
    #    $1: mode (CLI or REST)
    # side effects:
    #    - write output of docker into TESTDIR library
    #    - overwrite OUTPUT global variable
    #    - call spinner as backgroung process
    # return: none
    >&2 echo -n "- $1: " # log to stderr
    spin & spinpid=$! # start spinner
    disown $spinpid # https://stackoverflow.com/questions/8074904/how-to-shield-the-kill-output
    OUTPUT="${TESTDIR}/${1,,}_${BASENAME%.*}.tsv" # generate output filename
    if [ "$1" = "CLI" ] ; then
        date >$TESTDIR/log
        cat $INPUT | \
        docker run -i --rm mtaril/emtsv:test tok,morph,pos,conv-morph,dep >$OUTPUT 2>>$TESTDIR/log
    elif [ "$1" = "REST" ] ; then
        myport=$(find_free_port) 
        docker run --name emtsvtest -p ${myport}:5000 --rm -d mtaril/emtsv:test >/dev/null
        curl -F "file=@$INPUT" localhost:$myport/tok/morph/pos/conv-morph/dep >$OUTPUT 2>/dev/null
        docker container stop emtsvtest >/dev/null
    else
        return 1
    fi
    kill "$spinpid" # stop spinner
}


function mydiff {
    # Compare output of docker with gold.
    # parameters:
    #    $1: output file (file that should be compared with $GOLD)
    # return: result of test (textual message)
    local res="${GREEN}✔${NOCOLOR}"
    if [ "$(diff $GOLD $1)" ] ; then
        res="${RED}✘${NOCOLOR} (git diff --no-index --color-words $GOLD $1)"
    fi
    echo -e "\b$res"
}


## TEST CLI
run_docker 'CLI'
mydiff $OUTPUT

# ## TEST REST API
run_docker 'REST'
mydiff $OUTPUT

echo -e "See output files in $TESTDIR/ directory."
