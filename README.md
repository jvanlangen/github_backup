# github_backup
Cloning/updating all repositories from an organization daily to a local file system.

https://hub.docker.com/repository/docker/jvanlangen/github_backup

## Commandline

```
docker run \
    --name github_backup
    -e ORGANIZATION="<organization>" \
    -e ACCESS_TOKEN="<github_access_token>" \
    -e USERNAME="<username>" \
    -e EMAIL="<email>" \
    -e BACKUP_TIME="02:00" \
    -e TIMEZONE="Europe/Amsterdam"
    -v <local_path>:/data \
    jvanlangen/github_backup:latest
```

## Docker compose
```  
version: '3'

services:
  github_backup:
    image: jvanlangen/github_backup:latest
    container_name: github_backup
    environment:
      - ORGANIZATION=<organization>
      - ACCESS_TOKEN=<github_access_token>
      - USERNAME=<username>
      - EMAIL=<email>
      - BACKUP_TIME=02:00
      - TIMEZONE="Europe/Amsterdam"
    volumes:
      - <local_path>:/data
```
