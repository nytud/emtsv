#! /bin/bash

echo 'Test "mtaril/emtsv:test" docker image.'

RED="\033[1;31m"
GREEN="\033[1;32m"
NOCOLOR="\033[0m"

TESTDIR=$(mktemp -d /tmp/dtestXXXXXX)
INPUT='test/input/alaptorveny.txt'
GOLD='test/gold/alaptorveny_dep.tsv'
BASENAME=$(basename $INPUT)


function find_free_port {
    # parameters: no
    # return: free port number
    res=""
    for port in {10001..15000} ; do
        (echo '' >/dev/tcp/localhost/$port) >/dev/null 2>&1 || { res=$port; break; } ;
    done
    echo "$res"
}


function mydiff {
    # parameters:
    #    $1: mode (cli or rest)
    #    $2: output file (file that should be compared with $GOLD)
    # return: result of test (textual message)
    local res="${GREEN}passed${NOCOLOR}"

    if [ "$(diff $GOLD $2)" ] ; then
        res="${RED}failed${NOCOLOR}"
        git diff --no-index $GOLD $2 >${2%.*}.diff
        git diff --no-index --color-words $GOLD $2 >${2%.*}.color.diff
    fi
    echo -e "\nDocker $1 test $res (see output files in $TESTDIR/ directory)."
}

function get_output {
    # parameters:
    #    $1: mode (cli or xml)
    # return: name of output file
    OUTPUT="${TESTDIR}/${1,,}_${BASENAME%.*}".tsv
    if [ "$1" = "CLI" ] ; then
        LOG="$TESTDIR/log"
        date >$LOG
        cat $INPUT | \
        docker run -i --rm mtaril/emtsv:test tok,morph,pos,conv-morph,dep >$OUTPUT 2>>$TESTDIR/log
    elif [ "$1" = "REST" ] ; then
        myport=$(find_free_port) 
        docker run --name emtsvtest -p ${myport}:5000 --rm -d mtaril/emtsv:test >/dev/null
        curl -F "file=@$INPUT" localhost:$myport/tok/morph/pos/conv-morph/dep >$OUTPUT
        docker container stop emtsvtest >/dev/null
    else
        return 1
    fi
    echo $OUTPUT
}

# echo -e $(get_output 'CLI')
# echo -e $(get_output 'REST')
# echo -e $(get_output 'valami')

## TEST CLI
# echo -e '\n1. CLI'
# OUTPUT=$(get_output 'CLI')
# echo $OUTPUT
# echo -e "$(mydiff 'CLI' ${OUTPUT})"

# OUTPUT="${TESTDIR}/cli_${BASENAME%.*}".tsv
# LOG="$TESTDIR/log"
# date >$LOG
# cat $INPUT | \
# docker run -i --rm mtaril/emtsv:test tok,morph,pos,conv-morph,dep >$OUTPUT 2>>$TESTDIR/log
# echo -e "$(mydiff 'CLI' ${OUTPUT})"


## TEST REST API
echo -e '\n2. REST API'
OUTPUT=$(get_output 'REST')
echo $OUTPUT
# echo -e "$(mydiff 'REST' ${OUTPUT})"

# OUTPUT="${TESTDIR}/rest_${BASENAME%.*}".tsv

# myport=$(find_free_port) 
# docker run --name emtsvtest -p ${myport}:5000 --rm -d mtaril/emtsv:test >/dev/null
# curl -F "file=@$INPUT" localhost:$myport/tok/morph/pos/conv-morph/dep >$OUTPUT
# docker container stop emtsvtest >/dev/null
# echo -e "$(mydiff 'REST API' ${OUTPUT})"
