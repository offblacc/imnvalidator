#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <scheme.imn> <tests.json>"
    exit 1
fi

file1=$1
file2=$2

if [ ! -f "$file1" ]; then
    echo "Error: $file1 not found."
    exit 1
fi

if [ ! -f "$file2" ]; then
    echo "Error: $file2 not found."
    exit 1
fi

python3 py/validate.py $file1 $file2