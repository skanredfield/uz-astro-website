# uz-astro-website
UZ telescope monitoring website.

Postgres, nginx, and gunicorn can be configured according to this guide:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04

Database credentials that are encountered in the .env file should also be set as environmental or system variables.

The main directory, astrosite, contains the setting.py file. List of allowed hosts can be found in it. Add the appropriate address there to make sure the site can redirect its pages properly.
