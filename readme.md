# Shitty.in
### A project to be located at http://shitty.in


The purpose of this project is to explore Flask by building a web app to be placed at the domain shitty.in.  There is no real purpose for this project, it just takes up space on the internet and contributes minimally.


# Contributing

Feel free to contribute.



# Deploying to Digital Ocean

[Based on this guide](https://blog.marksteve.com/deploy-a-flask-application-inside-a-digitalocean-droplet/)

```
useradd -r -m -s /bin/bash deploy
apt-get install python3 python3-pip vim git
apt-add-repository ppa:nginx/stable
apt-get update
apt-get install nginx
pip3 install virtualenv

su - deploy

git clone https://github.com/patleeman/shitty.in.git

# Create and activate virtual environment
cd shitty.in
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
pip3 install gunicorn

# Create SECRETS.py
touch SECRETS.py
echo "SECRET STUFF" > SECRETS.py

# Test app
gunicorn -b 0.0.0.0:8000 wsgi

# Configure nginx
vim /etc/nginx/conf.d/shittyin.conf
```

Paste this into the conf file.
```
server {
    listen 80;

    server_name shitty.in;

    access_log  /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    location / {
        proxy_pass         http://127.0.0.1:8000/;
        proxy_redirect     off;

        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
    }
}
```

Edit nginx.conf and comment out ```include /etc/nginx/sites-enabled/*;```
```
vim /etc/nginx/nginx.conf
```

Finally run gunicorn

```
gunicorn -D wsgi
```
