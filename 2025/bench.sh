if [ -z $1 ]; then
    echo "Must provide day"
else
    day=$1
fi

if [ -z $2 ]; then
    iter=20
else
    iter=$2
fi

echo Day $day average time over $iter runs

for x in $(seq 1 $iter); do
   ./day${day}.py >> tmp
   echo $x
done | tqdm --total=$iter >> /dev/null

grep -oE "Total elapsed:.*?([0-9.]*)ms" tmp | sed -E 's/[^0-9.]+//g' | awk '{s+=$1; n++} END {print s/n "ms"}'

rm tmp