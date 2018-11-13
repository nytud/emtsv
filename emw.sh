#! /bin/bash


# here-document
read -d '' USAGE <<- EOF
emw (e-magyar wrapper) reads from files, processes the text with the e-magyar
toolchain and writes to standard output.
USAGE: emw.sh [OPTION]... [FILE]...
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
    emw.sh input.txt
    emw.sh -t ner *.txt
EOF


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
        -h|--help)
            echo "$USAGE"
            exit 0
            ;;
        *)
            if [[ -f "$1" ]] ; then
                FILES+=" $1"
            else
                echo "$0: $1: No such file or directory! Exit."
                exit 1
            fi
            shift
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
        MODULES='morph,pos,deptool,dep'
        ;;
    # con)
    #     MODULES=''
    #     ;;
    # npc)
    #     MODULES=''
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
    CMD="python3 emTSV20.py $MODULES"
fi


for file in $FILES; do
    { echo 'string' ; ./emtokenpy/bin/quntoken -f vert $file ; } | $CMD
done


