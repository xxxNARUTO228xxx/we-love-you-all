# Backend.  


Написан на [FastAPI](https://fastapi.tiangolo.com).


## Установка зависимостей  
```bash
pipenv shell

#Для инферентса на CPU:
pipenv install

#Для инференса на GPU, если стоит CUDA 11.7:
pip install -r requirements.txt

#Если версия CUDA отлична от 11.7, то необходимо изменить зависимости в requirements.txt:
https://pytorch.org/get-started/previous-versions/
```
## Модель

Модели доступны по ссылке:

```
https://disk.yandex.ru/d/IXNEekqbN7P01Q
```

Модель для детекции person и weapon
необходимо переместить в backend/yolo/ с названием "yolovX"

Чтобы добавить классификатор его необходимо поместить в backend/yolo/
c названием "yolovCLS"

## Запуск
Linux:
```bash
sh ./scripts/run.sh
```
  

Windows:  
```bash
./scripts/run.bat
```
