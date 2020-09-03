#!/bin/bash

INPUT_FILE='input.txt'

# Check if arguments passed are OK
if [ $# -le 0 ]
then
    echo "Usage: ./autocpp.sh <Program File> [<input-file>]"
    echo "
✳️ This script will compile the given file
✳️ Take input from ./input.txt or <input-file> and save to ./output.txt
✳️ If <verify-file> is provided then it compares with ./output.txt
"
    GCC_VERSION=`g++ --version | head -n1`
    echo "NOTE: Program file should compile using ${GCC_VERSION}"
    exit 1
fi

if [ "$#" -le "3" ]; then
    INPUT_FILE=$2
fi

if [ ! -f "$1" ]; then
    echo "Program File '$1' does not exist."
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Input File '$INPUT_FILE' does not exist."
    exit 1
fi


g++ -o program $1 -DLOCAL
ans=`./program < $INPUT_FILE`
echo "$ans" > output.txt
rm program

if [ "$#" -eq "3" ]
then
    if [ ! -f "$3" ]; then
        echo "Verify output '$3' does not exist."
        exit 1
    fi
    DIFF=`diff -b output.txt $3`
    if [ ! -z "${DIFF}" ]
    then
        echo "Sample Input"
        cat $INPUT_FILE
        echo ""
        echo ""
        echo "Sample Output"
        cat $3
        echo ""
        echo ""
        echo "Your output"
        echo $ans
        echo ""
        exit 1
    fi
fi

exit 0