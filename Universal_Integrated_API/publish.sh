#!/bin/bash
# 此脚本只适用于开发调试机器

cd `dirname $0`
echo "helloworld" | sudo -S python setup.py build
echo "helloworld" | sudo -S python setup.py sdist

if [[ $? -eq 0 ]] ; then
    echo "Publish Finished!"
    exit 0
else
    echo "Publish Failed!"
    exit 1
fi
