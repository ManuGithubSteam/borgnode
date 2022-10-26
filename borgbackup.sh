#!/bin/bash
BORGPW="m1s2"

if [ "$1" == "list" ];
  then
    BORG_PASSPHRASE=$BORGPW 
    sudo borgmatic list
fi
if [ "$1" == "backup" ];
    then
#    if [ ! -f backup-running ];
#        then
        echo "backup running" >  backup-running
        BORG_PASSPHRASE=$BORGPW 
        sudo borgmatic 
        rm backup-running
#    fi
fi

if [ "$1" == "extract" ];
  then
    BORG_PASSPHRASE=$BORGPW 
    echo "backup running" >  backup-running
    echo "$1 $2" >> extract.log
    sudo borgmatic extract --archive $2 --destination /Users/ms/recoverborg
    sudo chmod -R 777 /Users/ms/recoverborg/
    rm backup-running
fi
