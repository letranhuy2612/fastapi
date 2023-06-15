Project folder structure

```
FASTAPI/
├─ alembic/  <-- alembic folder & sub files
    ├─ versions/ 
    ├─ env.py
    ├─ README
    ├─ script.py.mako
├─ app/
    ├─ routers/
        ├─ auth.py
        ├─ file.py
        ├─ user.py 
    ├─ models
        ├─ models.py  
    ├─ utils
        ├─ minio_handler.py    
        ├─ oauth2.py
        ├─ utils.py  
    ├─ app.py
    ├─ config.py
    ├─ database.py
    ├─ schemas.py
├─ .env
├─ alembic.ini  <-- just added
├─ requirements.txt
├─ docker-compose.yml
├─ runserver.py

```
### Set Environment
```
docker compose up -d
```
### Database
Lần sử dụng đầu tiên
ta truy cập vào pgadmin được khởi tạo bởi docker compose truy cập vào localhost:5050 đăng nhập thông tin ở trong file docker-compose.yml
Thiết lập kết nối giữa pgadmin vs postgres như trong file docker-compose.yml
Sau đó tạo databasename như trong file .env
alembic là công cụ giúp việc migration database dễ dàng hơn
create a migration environment with the init command of alembic:
```
alembic init alembic
```
Sau lệnh này sẽ tạo ra folder chứa:
    versions/ - thư mục này chứa các tập lệnh phiên bản
    
    env.py – Nó chứa các hướng dẫn về cách định cấu hình và tạo công cụ SQLAlchemy.
    
    script.py.mako – a Mako template file that is used to generate new migration scripts within the versions folder.
 create a revision file with this command:
 
```
 alembic revision --autogenerate -m "create table"
```
chạy lệnh upgrade command đẩy các thay đổi vào cơ sở dữ liệu PostgreSQL.
```
alembic upgrade head
```
Sau đó ta truy cập vào pgadmin sẽ thấy các table sẽ được tạo 
### Run app

```
python runserve.py
```


