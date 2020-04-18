#bin/bash

file_paths=("$@")

echo '{"pages": [' > db.json
declare counter=1

for file_path in "${file_paths[@]}"
do
file_name=$(basename "$file_path") 
if [ $file_name != 'db.json' ]
then
    echo "{\"id\": $counter," >> db.json
    echo '"content": ' >> db.json
    cat $file_path >> db.json
    counter=$(($counter+1))
    echo '},' >> db.json
fi
done

echo ']}' >> db.json
