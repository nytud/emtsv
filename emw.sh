#! /bin/bash


# here-document
read -d '' USAGE <<- EOF
emw (e-magyar wrapper) reads from stdin, processes the text with the e-magyar
toolchain and writes to standard output.
USAGE: emw.sh [OPTION]...
OPTIONS:
    -h, --help           display this help and exit
    -t, --target TARGET  targeted level of analisys (default:all)
Valid targets:
    tok: sentence splitter and tokenizer
    mor: morphological analyser + word stemmer
    pos: POS tagger
    dep: dependency parser
    con: constituent parser
    npc: NP chunker
    ner: NER tagger
    all: all e-magyar modules are active (this is the default)
Examples:
    emw.sh <input.txt
    cat *.txt | emw.sh -t ner
EOF


MYDIR=$(dirname "$0")


# commandline arguments
while [[ $# -gt 0 ]]
do
    case "$1" in
        -t|--target)
            if [[ -z "$2" ]] ; then 
                echo "No given target! Exit."
                exit 1
            else
                TARGET="$2"
            fi
            shift
            shift
            ;;
        *)
            echo "$USAGE"
            exit 0
            ;;
    esac
done


# main target
if [[ -z $TARGET ]] ; then
    TARGET="all"
fi


# modules
case $TARGET in
    tok)
        MODULES=''
        ;;
    mor)
        MODULES='morph'
        ;;
    pos)
        MODULES='morph,pos'
        ;;
    dep)
        MODULES='morph,pos,conv-morph,dep'
        ;;
    # con)
    #     MODULES=''
    #     ;;
    # npc)
    #     MODULES='tok,morph,pos,chunk'
    #     ;;
    # ner)
    #     MODULES=''
    #     ;;
    all)
        MODULES='morph,pos,deptool,dep'
        ;;
    *)
        echo "'$TARGET' is not valid target! Exit."
        exit 1
        ;;
esac


if [[ -z $MODULES ]] ; then
    CMD="cat -";
else
    CMD="python3 ${MYDIR}/emTSV20.py $MODULES"
fi


cat - |  { echo 'string' ; python3 ${MYDIR}/emtokenpy/quntoken/quntoken.py ; } | $CMD
