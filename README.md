# storagetiers
[smh]

## Set-up this project

Run `docker-compose up` in terminal. You will need to install docker.

## API endpoints
Permisions to images - all users uploaded pictures are private (users can view only their pictures) unless user decides to share image for given amount of time. Then temporary link is generated and image is made available to everyone that has this link.

### /api/pictures

#### GET

Returns all Pictures uploaded by logged-in user

Success code: ```200```

Error code: ```403```

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

Example input:

```
{
   "name":"example_name"
   "img":"image.jpg",
}
```

Error codes:

```
400 - bad request

403 - authorization error 
```

### /api/pictures/shared/

#### GET

Returns list of images shared by user

Success code: `201`

Error code: ```403```

Example output:

````
[
   {
        "url": "/api/timelink/cc0f072e-ff1a-4691-aa55-9bade77a7a11",
        "picture": {
            "owner": 1,
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
        "owner": 1,
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
403 - authorization error
```

### /api/timelink/{uuid}

#### GET

Returns shared image with given uuid.

Success code: `200`

Error code: `404 - not found`

