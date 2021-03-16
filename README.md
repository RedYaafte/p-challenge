For this project.
Setup .env from .env.examples

Run project ```docker-compose up```

---

Run tests:

```
docker exec -it <container_name> bash
. venv/bin/activate
./manage.py test
```

API REST

* For create users:

```/api/user/```

```
email: str
name: str
```


* For create orders:

```/api/order/```

```
client: str
products: list
    name: str
    price: float
    qty: int
total_price: float
user_email: str
```

* For get reports:

```/api/report/?start-date=<YYYY-MM-DDThh:mm:ss>&end-date=<YYYY-MM-DDThh:mm:ss>```

* For create, get, update or delete products:

```/api/product/```

```
name: str
price: float
```