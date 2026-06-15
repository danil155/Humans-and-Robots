# Humans-and-Robots

## Развертка (dev mode)

1. Убедитесь в том, что у вас установлен `Docker Compose v2`:
    ```bash
    docker compose version
    ```

    В случае, если он не установлен:
    ```bash
    # Windows
    Скачайте по ссылке: https://docs.docker.com/desktop/setup/install/windows-install/
    
    # Ubuntu
    sudo apt-get install docker-compose-v2
    ```
2. Запустите
    ```bash
    docker compose up -d --build
    ```

   Для отслеживания логов контейнеров:
    ```bash
    docker compose logs -f
    ```

После этого сервис будет доступен по ссылке `http://localhost:3000`
