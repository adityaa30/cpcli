g++ -o program $1
start=$(($(date +%s%N)/1000000))
ans=`./program < input.txt`
end=$(($(date +%s%N)/1000000))
echo "$ans" > output.txt
echo $ans
echo "\nTime of execution: $(($end - $start))"
rm program
