#!/bin/bash
sed "s/\([.,;:?!]\)/ \1/" | tr ' ' '\n'
