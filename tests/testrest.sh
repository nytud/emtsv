#!/bin/bash

# make target for testing (test-...)
T=tok-morph-tag
# input file for testing
I=test_input/input.test
# output file during testing
O=out.input.tok-morph-tag.rest
# gold output for diff
G=test_output/out.input.tok-morph-tag
# message
M="using REST API"

# for REST API modules should be separated by '/' + tag->pos
TR=`echo $T | sed "s/-/\//g;s/tag/pos/"`

echo "Testing '$T' on '$I' $M"
echo "Be sure that the server has been started!"
python3 ./testrest.py $TR $I > $O
if diff $G $O; then
  echo "Test succeeded! :)"
else
  echo ">>> Test failed! :( <<<"
fi

