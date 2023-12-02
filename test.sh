db="tarkov"
qnum=1


for (( i=1; i<=$qnum; i++ ))
do
    sqlite3 $db < test/$i.sql > output/$i.out
done
