docker setup
```
docker volume create mysql_data

docker run -d \
    --name mysql_container \
    -e MYSQL_ROOT_PASSWORD=your_root_password \
    -e MYSQL_DATABASE=your_database_name \
    -e MYSQL_USER=your_username \
    -e MYSQL_PASSWORD=your_password \
    -p 3308:3306 \
    -v mysql_data:/var/lib/mysql \
    mysql:latest
```


sample query
```
các công ty product thì hay tuyển ngôn ngữ gì, và các công ty outsource hay tuyển ngôn ngữ gì ?
```

```
có bao nhiêu công ty outsource và có bao nhiêu công ty product ?
Trả lời: Có 248 công ty thuộc loại IT Product và 41 công ty thuộc loại IT Outsourcing.
```

```
Câu hỏi của bạn: trả lời cho tôi có bao nhiêu java job open và lương trung bình và bao nhiêu job python đang open và lương trung bình
Có 72 công việc Java đang mở và 30 công việc Python đang mở. Tuy nhiên, do cơ sở dữ liệu không chứa thông tin về lương, tôi không thể cung cấp thông tin về mức lương trung bình cho các công việc này.
```