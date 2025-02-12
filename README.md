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
	menu_name text NOT NULL,
	member_name text NOT NULL,
	dt date NOT NULL,
	CONSTRAINT lunch_menu_pk PRIMARY KEY (id)
);

alter table lunch_menu
add constraint unique_member_dt unique (member_name, dt);
```

## Dev
```bash
# DB Check, Start, Stop
$ sudo docker ps -a
$ sudo docker start local-postgres
$ sudo docker stop local_postgres
```

- RUN
```bash
# 디비 정보에 맞춰 수정
& cp env.dummy .env

# 서버 시작
$ streamlit run App.py
```

