# t0url

## Website

[url.t0.vc](https://url.t0.vc)

## Description

Command line URL shortener.

This allows you to submit URLs from your command line or browser. A short URL is returned.

## Usage

`<command> | curl -F 'url=<-' https://url.t0.vc`

You can also submit from the web at [url.t0.vc](https://url.t0.vc).

## Example

```text
$ cat yourfile | curl -F 'url=<-' https://url.t0.vc
  https://url.t0.vc/VFAR
$ firefox https://url.t0.vc/VFAR
```

### Bash Alias

Add this to your .bashrc, then `source ~/.bashrc`:

```text
alias url="curl -F 'url=<-' https://url.t0.vc"
```

Now you can pipe a URL directly into url!

```text
$ cat yourfile | url
  https://url.t0.vc/VFAR
$ firefox https://url.t0.vc/VFAR
```

## Self-hosting

Install dependencies:
```text
$ sudo apt install python3 python3-pip python-virtualenv python3-virtualenv
```

Clone repo, create a venv, activate it, and install:
```text
$ git clone https://github.com/tannercollin/t0url.git
$ cd t0url
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

You can now run it directly:
```text
(env) $ python t0url.py
```

It's recommended to run t0url as its own Linux user, kept alive with [supervisor](https://pypi.org/project/supervisor/):
```text
[program:t0url]
user=t0url
directory=/home/t0url/t0url
command=/home/t0url/t0url/env/bin/python -u t0url.py
autostart=true
autorestart=true
stderr_logfile=/var/log/t0url.log
stderr_logfile_maxbytes=1MB
stdout_logfile=/var/log/t0url.log
stdout_logfile_maxbytes=1MB
```

To expose t0url to http / https, you should configure nginx to reverse proxy:
```text
server {
    listen 80;

    root /var/www/html;
    index index.html index.htm;

    server_name url.t0.vc;

    location / {
        proxy_pass http://127.0.0.1:5002/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then run `sudo certbot --nginx` and follow the prompts.

## See Also

Pastebin: [txt.t0.vc](https://txt.t0.vc) - [Source Code](https://github.com/tannercollin/t0txt)

Image host: [pic.t0.vc](https://pic.t0.vc) - [Source Code](https://github.com/tannercollin/t0pic)

## License
This program is free and open-source software licensed under the MIT License. Please see the `LICENSE` file for details.

That means you have the right to study, change, and distribute the software and source code to anyone and for any purpose. You deserve these rights. Please take advantage of them because I like pull requests and would love to see this code put to use.

## Acknowledgements

Thanks to all the devs behind Flask and Python.
