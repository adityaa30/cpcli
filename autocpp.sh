# Check if arguments passed are OK
if [ $# != 1 ]
then
    echo "Usage: ./autocpp.sh <Program File>"
    echo "
✳️ This script will compile the given file
✳️ Take input from ./input.txt and save to ./output.txt
✳️ At the end approximate time of execution is also shown
"
    GCC_VERSION=`g++ --version | head -n1`
    echo "NOTE: Program file should compile using ${GCC_VERSION}"
    exit 0
fi


if [ ! -f "$1" ]; then
    echo "Program File '$1' does not exist."
    exit 0
fi

g++ -o program $1 -DLOCAL
start=$(($(date +%s%N)/1000000))
ans=`./program < input.txt`
end=$(($(date +%s%N)/1000000))
echo "$ans" > output.txt
echo $ans
echo "\nTime of execution: $(($end - $start)) ms"
rm program
