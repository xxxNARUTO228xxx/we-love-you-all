# Backend.  


Написан на [FastAPI](https://fastapi.tiangolo.com).


## Установка зависимостей  
```bash
pipenv shell

#Для инферентса на CPU:
pipenv install

#Для инференса на GPU, если стоит CUDA 11.7:
pip install -r requirements.txt

#Если версия CUDA отлична от 11.7, то необходимо изменить зависимости:
https://pytorch.org/get-started/previous-versions/
```
## Модель

Модель для детекции person и weapon
необходимо переместить в backend/yolo/ с названием "yolovX"
  
## Запуск  
Linux:
```bash
sh ./scripts/run.sh
```
  

Windows:  
```bash
./scripts/run.bat
```
