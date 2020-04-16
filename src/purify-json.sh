#bin/bash

file_paths=("$@")
temp_file='/tmp/webcrawler_bol.json'

for file_path in "${file_paths[@]}"
do
file_name=$(basename "$file_path")
  
cat $file_path | 
sed -E 's/"_([a-zA-Z|_]+)"/"\1"/' | 
sed -E 's/"\\n */"/' | 
sed -E 's/\\n *",$/",/' | 
sed -E 's/\\u[a-zA-Z0-9]+//g' > $temp_file

cp $temp_file $file_path
done
