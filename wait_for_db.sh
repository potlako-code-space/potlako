#!/bin/sh
# wait-for-mysql.sh

set -e

host="$1"
shift
user="$1"
shift
password="$1"
shift
cmd="$@"
db="${MYSQL_DB_NAME}"

until mysql -h "$host" -u "$user" --password="$password" -e "use $db"; do
 >&2 echo "MySQL is unavailable - sleeping"
 sleep 1
done

>&2 echo "MySQL is up - executing command"

exec $cmd