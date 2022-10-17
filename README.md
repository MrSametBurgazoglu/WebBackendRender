# WebBackendRender

Araç Kiralama Web Backend

API url:https://carrentrestwebbackendapi.onrender.com/api/

# User işlemleri

### create user
```
self.client.post("/api/accounts/customers/", {
            "name": "SametBurgazoğlu",
            "phone": "123213123",
            "email": "sametburgazoglu@gmail.com",
            "password": "54M3754m37",
        },
                               content_type="application/json")
```

### get token
```
self.client.post("/api/accounts/api-token-auth/", {
            "email": "sametburgazoglu@gmail.com",
            "password": "54M3754m37",
        },
                                    content_type="application/json")
```

### update user
```
WARNING: Need Token Authentication
self.client.put("/api/accounts/customers/{user_id}/".format(user_id=user.id), {
            "name": "SametBurgazoğlu2",
            "phone": "1232131232",
            "email": "sametburgazoglu@gmail.com",
            "password": "54M3754m37",
        },
                                    content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
```


### delete user
```
WARNING: Need Token Authenticatio
nself.client.delete("/api/accounts/customers/{user_id}/".format(user_id=user.id),
                                      content_type="application/json",
                                      **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
```

# Araç işlemleri
WARNING: bütün işlemler token authentication gerektiriyor
### get cars nearby
```
self.client.get("/api/cars/", {
            "latitude": "1",
            "longitude": "1",

        },
                                    content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
```

### get car detail
```
self.client.delete("/api/accounts/customers/{user_id}/".format(user_id=user.id),
                                      content_type="application/json",
                                      **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
```

### delete car
```
self.client.delete("/api/cars/{id}/".format(id=first_car.id),
                                   content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
```

### change car active state
```
self.client.post("/api/cars/{id}/change_state/".format(id=first_car.id),
                                   content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
```

