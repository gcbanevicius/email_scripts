#!/bin/bash

cd ~/Desktop

cat passes_simple.txt |
while read line; do
    count=$(grep -c $line passes_simple.txt)
    if [ $count -gt 1 ]; then
        echo $line, $count
    fi
done
