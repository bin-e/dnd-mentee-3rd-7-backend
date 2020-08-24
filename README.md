### D&D 3기 7조 README

* [위키 이동](https://github.com/dnd-mentee-3rd/dnd-mentee-3rd-7-repo/wiki)
* [노션 바로가기](https://www.notion.so/Index-eb8608900f264739af9c330b4e7c7b29)

--- 

### Project setup 

```
docker-compose -f docker-compose.yml up -d --build
docker-compose -f docker-compose.yml exec django python manage.py migrate --noinput
docker-compose -f docker-compose.yml exec django python manage.py collectstatic --no-input --clear
```


test







