#!/usr/bin/env bash
# 启动主任务

while getopts ":q:c:n:m:l:" opt; do
  case $opt in
  q) queue_name=$OPTARG;;
  c) concurrency=$OPTARG;;
  n) worker_name=$OPTARG;;
  m) max_tasks_per_child=$OPTARG;;
  l) log_level=$OPTARG;;
  ?) echo "未知参数"
    exit 1;;
  esac
done

if [ ! ${queue_name} ]; then exit 1; fi
if [ ! ${concurrency} ]; then exit 1; fi
if [ ! ${worker_name} ]; then exit 1; fi


rabbitmq_host='rabbitmq:15672'
admin_user='guest'
admin_password='guest'


alive_code=`curl -i -u $admin_user:$admin_password -H "content-type:application/json" -I -m 10 -o /dev/null -s -w %{http_code} http://${rabbitmq_host}/api/vhosts | grep -v %`
add_host_code=`curl -i -u $admin_user:$admin_password -H "content-type:application/json" -I -m 10 -o /dev/null -s -w %{http_code} -XPUT http://${rabbitmq_host}/api/vhosts/%2Fbore | grep -v %`
add_user_code=`curl -i -u $admin_user:$admin_password -H "content-type:application/json" -m 10 -o /dev/null -s -w %{http_code} -XPUT -d'{"password":"bore","tags":"administrator"}' http://${rabbitmq_host}/api/users/bore | grep -v %`
add_permission_code=`curl -i -u $admin_user:$admin_password -H "content-type:application/json" -m 10 -o /dev/null -s -w %{http_code} -XPUT -d'{"configure":".*","write":".*","read":".*"}' http://${rabbitmq_host}/api/permissions/%2Fbore/bore | grep -v %`
echo "add_host_code" $add_host_code
echo "add_user_code" $add_user_code
echo "add_permission_code" $add_permission_code

if [ $alive_code -eq 200 ]; then
  echo "rabbitmq service alive"
  if [ $add_host_code -eq 204 ] || [ $add_host_code -eq 200 ]; then
    echo "host added"

    if [ $add_user_code -eq 204 ] || [ $add_user_code -eq 200 ]; then
      echo "user added"

      if [ $add_permission_code  -eq 204 ] || [ $add_permission_code -eq 200 ]; then
        echo "permission added"
        celery -A celery_server worker -n ${worker_name}@%h -c ${concurrency} -l ${log_level} -Q ${queue_name} --max-tasks-per-child ${max_tasks_per_child}
      else
        exit
      fi
    else
      exit
    fi
  else
    exit
  fi
else
  exit
fi
