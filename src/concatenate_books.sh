#bin/bash

file_paths=("$@")

echo '{"books": [' > /tmp/bookdb.json

for file_path in "${file_paths[@]}"
do
file_name=$(basename "$file_path") 
if [ $file_name != 'db.json' ]
then
    cat $file_path | head -n -1 | tail -n +2 >> /tmp/bookdb.json
    echo ',' >> /tmp/bookdb.json
fi
done

echo ']}' >> /tmp/bookdb.json
cp /tmp/bookdb.json .
