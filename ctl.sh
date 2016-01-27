#!/bin/bash
# 
# 2016/1/27

source_path='/opt/charade'

function do_online(){
    # find /opt/charade/www/ ! -user nobody -print
    n=`find "${source_path}/www" ! -user nobody -print |wc -l`
    if [ $n -eq 0 ]; then
        echo '[-] Up to date!'
    else
        echo '[-] List the files that should chown to nobody:'
        find "${source_path}/www" ! -user nobody -print
        chown nobody:nobody -R "${source_path}/www"
        do_reload
    fi
}

function do_static(){
    cd "${source_path}/www"
    python manage.py collectstatic
}

function do_test(){
    cd "${source_path}/www"
    python manage.py test
}

function do_reload(){
    supervisorctl status
    supervisorctl reload
    sleep 2
    supervisorctl status
}

function usage(){
    cat <<_EOF

USAGE: $0 [static|test|online|reload] 

    static  :     collectstatic
    test    :     test
    online  :     chown to nobody and reload
    reload  :     reload supervisor

_EOF
}

case $1 in
    static|test|online|reload)
        do_$1
        ;;
    *)
        usage
        ;;
esac
