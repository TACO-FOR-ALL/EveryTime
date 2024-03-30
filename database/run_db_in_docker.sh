# 작성자: Macchiato
# 먼저 Docker Hub에서 알맞은 버젼의 MySQL image를 PULL하고 진행

docker run \
--name taco_dev_db \
-e MYSQL_ROOT_PASSWORD=123456 \
-e TZ=Asia/Shanghai \
-v TACO_DEV_VOLUME:/var/lib/mysql \
-p 127.0.0.1:3306:3306 \
mysql:8.0.36-debian
#-p 127.0.0.1:33060:330606 \
# image tag는 실제 사용하는 tag에 따라 수정