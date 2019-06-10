#!/bin/bash
# 此脚本只适用于开发调试机器,并且应和安装包放置于同一目录下,该目录只能包含一个安装包
cd `dirname $0`
username=`whoami`

install_pacakge=`ls | grep ".tar.gz"`
a=`pip install $install_pacakge 1>/dev/null 2>/dev/null; echo $?`
b=`pip3 install $install_pacakge 1>/dev/null 2>/dev/null; echo $?`
if [[ $a == 0 ]] ; then
    echo "Install package successful by pip."
fi
if [[ $b == 0 ]] ; then
    echo "Install package successful by pip3."
fi
if [[ $a != 0 ]] || [[ $b != 0 ]] ; then
    echo "pip/pip3 not installed successful. Go on installing by setup.py"
else
    echo "jcu install successful by pip&pip3"
    exit 0
fi

# 解压安装包
tar -zxvf $install_pacakge
if [[ $? == 0 ]]; then
    # python setup.py install 方式安装
    cd `ls | sed -n "1p"`
    if [[ $username == "gdlocal" ]]; then
        echo "gdlocal" | sudo -S python setup.py install
    elif [[ $username == "coreos" ]]; then
        echo "helloworld" | sudo -S python setup.py install
    elif [[ $username == "cyril" ]]; then
        cat ~/passwd.txt | sudo -S python setup.py install
    fi

fi
echo "jcu install successful by setup.py"
