#! /bin/bash

HOSTNAME='127.0.0.1'
PORT='8080'

# Set the hostname and port (if given)
if [ $# == 2 ]; then
    HOSTNAME=$1
    PORT=$2
fi

for req in *.request; do
    echo "Testing: $req"
    echo
    nc $HOSTNAME $PORT < $req
    echo "------------------------"
done
