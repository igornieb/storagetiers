# storagetiers
[smh]

## Set-up
You will need to install docker.

Run terminal in project directory and type `docker compose up`.

## API endpoints
Permissions to images - all users uploaded pictures are private (users can view only their pictures) unless user decides to share image for given amount of time (create specific link). Then temporary link is generated and image is made available to everyone that has this link.

Authentication - JWT token is used for authentication across API views.

### /api/token/

#### POST

Returns access and refresh tokens

Success code: ```200```

Error code: ```401 - authentication error```

Example input:
```
{
    "username": "user",
    "password": "user_password"
}
```

Example output:
```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NzA3MzU3OSwiaWF0IjoxNjc2OTg3MTc5LCJqdGkiOiIzNzUzOGZkYjJkNWM0NmM5YmE1NjhiMDVlZjg2MTM3ZiIsInVzZXJfaWQiOjF9.mp8xlGAkUoBDDZg1gAzWF2fuok685lv5ZVDtRfwYCQk",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc2OTg4Mzc5LCJpYXQiOjE2NzY5ODcxNzksImp0aSI6ImMyZDVmMTIxNGFkODRhZDJiMzQ2NmU1ZWNjNjhhOGM4IiwidXNlcl9pZCI6MX0.nSFZqaG0Hd1AVjWsruYFudznSJVxKwNsAuVW64NMxpc"
}
```

### /api/token/refresh/

#### POST

Returns new access token

Success code: ```200```

Error code: ```401 - Token is invalid or expired```

Example input:
```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NzA3MzU3OSwiaWF0IjoxNjc2OTg3MTc5LCJqdGkiOiIzNzUzOGZkYjJkNWM0NmM5YmE1NjhiMDVlZjg2MTM3ZiIsInVzZXJfaWQiOjF9.mp8xlGAkUoBDDZg1gAzWF2fuok685lv5ZVDtRfwYCQk"
}
```
Example output:
```
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc2OTg5MTcyLCJpYXQiOjE2NzY5ODcxNzksImp0aSI6IjVlYTBjMmQxOGZmMjRkNTA4ODBiNjNhOTkxOTA5ODU1IiwidXNlcl9pZCI6MX0.sULHx8PqzRINhdZrpS0B806ZSi_Cs1vcsSLSOGRee_k"
}
```

### /api/pictures

#### GET

Returns all Pictures uploaded by logged-in user

Success code: ```200```

Error code: ```401 - authentication error```

Example output:
```
[
   {
        "owner": 1,
        "name": "honda hrc poster",
        "urls": "['/api/picture/e7362eca-382b-4204-9531-23469b18dbcc/200', '/api/picture/e7362eca-382b-4204-9531-23469b18dbcc/400', '/api/picture/e7362eca-382b-4204-9531-23469b18dbcc']"
    }
    ...
]
```


#### POST

Uploads new Picture

Success code: `201`

Error codes:
```
400 - bad request

401 - authentication error 
```

Example input:

```
{
   "name":"example_name"
   "img":"image.jpg",
}
```
Example output:
```
{
    "owner": "admin",
    "name": "test",
    "urls": "['/api/picture/b8ce8d79-e07c-43e3-af3e-51416946cfe3/200']"
}
```

### /api/pictures/shared/

#### GET

Returns list of images shared by user

Success code: `201`

Error code: ```401 - authentication error```

Example output:

````
[
   {
        "url": "/api/timelink/cc0f072e-ff1a-4691-aa55-9bade77a7a11",
        "picture": {
            "owner": admin,
            "name": "honda hrc poster",
            "urls": "['/api/picture/e7362eca-382b-4204-9531-23469b18dbcc/200', '/api/picture/e7362eca-382b-4204-9531-23469b18dbcc/400', '/api/picture/e7362eca-382b-4204-9531-23469b18dbcc']"
        },
        "time": 400,
        "time_left": "Expired"
   },
   ...
]
````

### /api/picture/{id}

#### GET

Returns image with given uuid in its original resolution if owner's tier allows viewing in full resolution.

Success code: `200`

Error codes:

```
403 - authorization error
403 - user Tier doesnt allow for this resolution
```

#### POST

Creates temporary link (available for specified amount of time from 300 to 30000 seconds) to image with given uuid.

Success code: `200`


Example input:
```
{
   "time":"400",
}
```

Example output:
``
{
    "url": "/api/timelink/0363825a-cb79-45d3-8d93-fbf8118c701b",
    "picture": {
        "owner": admin,
        "name": "honda hrc poster",
        "urls": "['/api/picture/e7362eca-382b-4204-9531-23469b18dbcc/200', '/api/picture/e7362eca-382b-4204-9531-23469b18dbcc/400', '/api/picture/e7362eca-382b-4204-9531-23469b18dbcc']"
    },
    "time": 400
}
``

### /api/picture/{pk}/{height}

#### GET

Returns image with given uuid in its original resolution if owner's tier allows viewing in full resolution.

Success code: `200`

Error codes:

```
403 - user Tier doesnt allow for this resolution
401 - authentication error
```

### /api/timelink/{uuid}

#### GET

Returns shared image with given uuid.

Success code: `200`

Error code: `404 - not found`

