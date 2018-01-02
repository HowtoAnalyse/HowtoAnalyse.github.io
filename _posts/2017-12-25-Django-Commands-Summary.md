---
layout: page
sidebar: right
title: "Commands Cheat Sheet"
subheadline: ""
teaser: ""
tags:
  - Django
categories:
  - Toolbox
---

```shell
# Start new django project and app
$ django-admin.py startproject mysite
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py startapp myapp

# Run jango
$ ./manage.py shell
$ ./manage.py runserver

# django migration
$ ./manage.py makemigrations myapp
$ ./manage.py sqlmigrate myapp 0001
$ ./manage.py migrate
$ ./manage.py squashmigrations myapp 0004

# django database backup & restore
$ ./manage.py dumpdata --indent 2 --exclude auth.permission --exclude contenttypes > db.json
$ ./manage.py loaddata db.json

# sqlite3
$ sqlite3 db.sqlite3
sqlite> .tables

# test
from django.test.utils import setup_test_environment
setup_test_environment()
$ python manage.py test myapp

# Distribution
$ python setup.py sdist
$ pip install django-package-0.1.tar.gz
```