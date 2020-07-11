#!/bin/bash
IFS=$'\n'; set -f

CPP_FILES=`find . -name '*.cpp'`
TEST_PROG_FILE=`head /dev/urandom | tr -dc A-Za-z0-9 | head -c 10 ; echo ''`

TEST_EXIT_STATUS=0

echo "Checking if all *.cpp files compiles successfully 🙃"

for path in $CPP_FILES
do
    # To support programs using pthread we add flag
    # TODO: Use pthread flag only when required
    g++ $path -o $TEST_PROG_FILE -pthread

    if [ -f $TEST_PROG_FILE ];
    then
        echo "$path: ✅"
        rm $TEST_PROG_FILE
    else
        echo "$path: ❌"
        TEST_EXIT_STATUS=1
    fi
done

unset IFS; set +f

exit $TEST_EXIT_STATUS