### На одном из серверов выполните команду:

```bash
docker swarm init
docker swarm init --advertise-addr 192.168.0.2
```
Это создаст кластер Swarm и выдаст команду для добавления других узлов.


### На втором сервере выполните команду, которую вы получили на первом сервере (что-то вроде):

```bash
docker swarm join --token <token> <manager-ip>:<port>
```

### Скопировать все файлы на основной сервер
### Создать файл .env


### Собрать образ
```shell
docker compose build
```

### Разверните стек: На главном сервере выполните команду:

```bash
docker stack deploy -c docker-compose.yml <имя_стека>
```
Замените <имя_стека> на желаемое имя для вашего стека.


### После развертывания вы можете проверить состояние сервисов:

```bash
docker stack services <имя_стека>
```

> Если вы используете переменные окружения из файла .env, убедитесь, что файл доступен на сервере.

### Чтобы увидеть, какие сервисы развернуты на каждом узле

```bash
docker service ls
```


### Для получения информации о конкретном сервисе, включая его реплики и узлы, на которых они запущены

```bash
docker service ps <имя_сервиса>
```


Чтобы указать, на каком сервере (узле) в кластере Docker Swarm запустить сервис, вы можете использовать параметр `--constraint` при создании сервиса с помощью команды `docker service create`. Этот параметр позволяет задать ограничения на размещение контейнеров.

Вот общий синтаксис команды:

docker node ls

docker save -o wb_bot_pro-grpc_celery.tar wb_bot_pro-grpc_celery:latest
scp -P 53 wb_bot_pro-grpc_celery.tar user@other-node:/path/to/save
ssh user@other-node
docker load -i /path/to/save/wb_bot_pro-grpc_celery.tar


# Читаем переменные из .env и создаем команду
env_file=".env"
env_vars=$(grep -v '^#' "$env_file" | sed 's/^/--env /')

# Создаем сервис с переменными среды
docker service create --name postgres --constraint 'node.hostname==ruvds-n9vme' $env_vars postges
# остановить
docker service update --replicas 0 postgres

docker volume create pg_data
docker service create \
  --name postgres \
  --constraint 'node.hostname==ruvds-n9vme' \
  --mount type=volume,source=pg_data,target=/var/lib/postgresql/data \
  $env_vars \
  postgres

docker volume create shared_volume
docker service create \
  --name grpc_celery \
  --replicas 1 \
  --mount type=volume,source=shared_volume,target=/app/grpc_app/shared \
  --mount type=volume,source=shared_volume,target=/app/celery_app/shared \
  grpc_celery


# Заходим в контейнер на втором сервисе
docker exec -it 7eae54b89e37 psql -U user -d db53
psql -h <IP-адрес_или_имя_узла> -p 5432 -U <имя_пользователя> -d <имя_базы_данных>





```bash
docker service create --name <имя_сервиса> --constraint 'node.hostname==<имя_узла>' <образ>
```

Например, если вы хотите создать сервис с именем `my_service`, который будет запущен на узле с именем `node1`, команда будет выглядеть так:

```bash
docker service create --name my_service --constraint 'node.hostname==node1' my_image
```

Здесь `my_image` — это имя образа, который вы хотите использовать для сервиса.

Также можно использовать другие типы ограничений, такие как `node.labels`, если вы хотите использовать метки узлов для более сложных сценариев размещения. Например:

```bash
docker service create --name my_service --constraint 'node.labels.mylabel==myvalue' my_image
```

Убедитесь, что узел, на котором вы хотите запустить сервис, доступен в вашем кластере Docker Swarm.