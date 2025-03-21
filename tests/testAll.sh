#!/bin/bash
dirs=$(ls -d */)
project_root="$(dirname "$(pwd)")"
echo $project_root
exit

for dir in $dirs; do
    sudo -E ../py/validate.py $dir/scheme.imn $dir/test_config.json -vt
    echo "Tests failed: $?"
done
