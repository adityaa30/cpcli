g++ -o program $1
start=$(($(date +%s%N)/1000000))
./program < input.txt
end=$(($(date +%s%N)/1000000))
echo "Time of execution: $(($end - $start))"
rm program

