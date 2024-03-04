# github_backup
Cloning/updaing all repositories from an organization to a local file system.

## Commandline

```
docker run -e ORGANIZATION="<organization>" -e ACCESS_TOKEN="<github_access_token>" -e USERNAME="<username>" -e EMAIL="<email>" -v <local_path>:/data -e BACKUP_TIME="02:00"  github_backup
```

## Docker compose
```  
version: '3'

services:
  github_backup:
    image: github_backup  # Vervang github_backup door de naam van je image
    environment:
      - ORGANIZATION=<organization>
      - ACCESS_TOKEN=<github_access_token>
      - USERNAME=<username>
      - EMAIL=<email>
      - BACKUP_TIME=02:00
    volumes:
      - <local_path>:/data
```
