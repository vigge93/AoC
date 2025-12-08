if [ -z $1 ]; then
    days=12
else
    days=$1
fi

echo $days

for x in $(seq 1 $days); do
   ./day${x}.py
done