# python-django-exercise

> Create two microservices using python django, and one will call another endpoint. This is following this video - [Python Microservices for Beginners](https://www.youtube.com/watch?v=rOpJhKa-Chk)

## Setup

> Install required libraries

```
pip install django djangorestframework django-cors-headers requests
```

## Create Two Folders

```
mkdir posts comments
```

## Generate projects in posts folder

```
cd posts
```

```
python3 -m django startproject app .
```

```
python3 -m django startapp core
```

## Prep posts microservice

### Update settings.py

> Update INSTALLED_APPS variable

```
    ...
    'rest_framework',
    'corsheaders',
    'core'

```

> Update MIDDLEWARE variable, cors middleware before common middleware

```
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
    
```

> Allow all frontends by adding CORS_ALLOW_ALL_ORIGINS variable

```
CORS_ALLOW_ALL_ORIGINS = True
```
> Setup database connections

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.1.240',
        'PORT': '30306',
        'NAME': 'posts_ms',
        'USER': 'root',
        'PASSWORD': 'password'        
    }
}
```

### Setup basic api paths

> Include core/urls.py in app/urls.py

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',admin.site.urls),
    path('api/',include('core.urls'))
]
```

> Stub core/urls.py

```
urlpatterns = [
]
```
## Copy everything to comments microservice folder

```
xcopy posts comments /s /e
```


## Test posts endpoint with curl

```
curl -X POST -H "Content-type: application/json" -d "{\"title\": \"title 1\", \"description\": \"description 1\"}" http://localhost:8000/api/posts
```

