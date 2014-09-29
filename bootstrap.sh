#!/bin/bash
virtualenv=virtualenv

function vercomp () { # Dennis Williamson http://stackoverflow.com/questions/4023830/bash-how-compare-two-strings-in-version-format
    if [[ $1 == $2 ]]
    then
        return 0
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++))
    do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++))
    do
        if [[ -z ${ver2[i]} ]]
        then
            # fill empty fields in ver2 with zeros
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]}))
        then
            return 1
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]}))
        then
            return 2
        fi
    done
    return 0
}

function create_virtualenv() {
#    if [ -x sandbox/bin/python ]
#    then
#        echo "reusing existing virtualenv"
#    else
        ${virtualenv} ${options} sandbox
	./sandbox/bin/pip install -U setuptools
        ./sandbox/bin/pip install numpy six python-dateutil tornado pyparsing
	./sandbox/bin/pip install matplotlib
#        ./sandbox/bin/pip uninstall -y setuptools
#    fi
}

function bootstrap() {
    create_virtualenv
    sandbox/bin/python bootstrap.py
}


bootstrap
