# github_backup
Cloning/updaing all repositories from an organization to a local file system.

## Commandline

```
docker run \
    -e ORGANIZATION="<organization>" \
    -e ACCESS_TOKEN="<github_access_token>" \
    -e USERNAME="<username>" \
    -e EMAIL="<email>" \
    -e BACKUP_TIME="02:00" \
    -v <local_path>:/data \
    jvanlangen/github_backup:latest
```

## Docker compose
```  
version: '3'

services:
  github_backup:
    image: jvanlangen/github_backup:latest
    environment:
      - ORGANIZATION=<organization>
      - ACCESS_TOKEN=<github_access_token>
      - USERNAME=<username>
      - EMAIL=<email>
      - BACKUP_TIME=02:00
    volumes:
      - <local_path>:/data
```
