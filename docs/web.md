# Kumir-Compose for web

## Как запустить example_web проект

Установить зависимости
```sh
cd example_web
kumir-compose install
```

Скомпилировать контроллеры
```sh
kumir-compose compile routes/index.kum
kumir-compose compile routes/ping.kum
kumir-compose compile routes/user-register.kum
```

Запустить веб-приложение
```sh
kumir-compose web -b 0.0.0.0:8000
```
