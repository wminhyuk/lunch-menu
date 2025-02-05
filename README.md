# lunch-menu
- [x]팀원들의 점심 메뉴를 수집
- []분석
- 알람(입력하지 않은 사람들에게 ...)
- CSV to DB

## Ready
### Install DB with Docker
- https://hub.docker.com/_/postgres
```bash
$ sudo docker run --name local-postgres \
-e POSTEGRES_USER=sunsin \
-e POSTEGRES_PASSWORD=mysecretpassword \
-e POSTGRES_DB=sunsindb \
-p 5432:5432 \
-d postgres:15.10
```

### Create Table
- postgres
```sql
CREATE TABLE public.lunch_menu (
    id serial NOT NULL,


## Dev
```bash
# DB Check, Start, Stop
$ sudo docker ps -a
$ sudo docker start local-postgres
$ sudo docker stop local_postgres


??
