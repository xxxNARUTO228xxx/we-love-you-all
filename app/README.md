# FindGun.

### Web-приложение

`./web`

# Docker 
Для сборки образа необходимо использовать:
```docker build -t findgun .
```  
Веб-сервис развернутый в Docker будет использовать для инференса CPU.

Для запуска контейнера:
```docker run -p 3000:3000 findgun:latest
```  
