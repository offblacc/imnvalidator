#!/bin/bash
#set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(dirname "$script_dir")"

for test_dir in "$script_dir"/*/; do
    if [ -f "${test_dir}scheme.imn" ] && [ -f "${test_dir}test_config.json" ]; then
        cmd="$project_root/py/validate.py ${test_dir}scheme.imn ${test_dir}test_config.json -vt"
        echo

        sudo -E "$project_root/py/validate.py" "${test_dir}scheme.imn" "${test_dir}test_config.json" --aggregate-run
        echo "Tests failed: $?"
    fi
done
