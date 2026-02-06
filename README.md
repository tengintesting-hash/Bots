# Telegram Web App Casino Ecosystem

Повний стек для Telegram WebApp + бот + бекенд.

## Вимоги
- Docker та Docker Compose.

### Як встановити Docker
- Windows/Mac: завантажте Docker Desktop з офіційного сайту https://www.docker.com/ і встановіть.
- Linux: використайте інструкцію для вашого дистрибутиву на сайті Docker.

## Запуск
1. Скопіюйте `.env.example` у `.env` та заповніть значення.
2. Запустіть сервіси:
   ```bash
   docker compose up -d
   ```
3. Якщо порт 8000 зайнятий, змініть `BACKEND_PORT` у `.env`.
4. Якщо бот не стартує, перевірте що `BOT_TOKEN` заповнений і перегляньте логи бота.

## Зупинка
```bash
docker compose down
```

## Перегляд логів
- Бекенд:
  ```bash
  docker compose logs -f backend
  ```
- Бот:
  ```bash
  docker compose logs -f bot
  ```
- Фронтенд:
  ```bash
  docker compose logs -f frontend
  ```

Також логи пишуться у папку `logs/`.

## Додавання каналів і оферів через curl
### Додати канал
```bash
curl -X POST http://localhost:8000/admin/channels \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: change_me_admin_token" \
  -d '{"channel_id": -1001234567890, "link": "https://t.me/channel", "title": "Супер канал", "is_required": true}'
```

### Додати офер
```bash
curl -X POST http://localhost:8000/admin/offers \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: change_me_admin_token" \
  -d '{"title": "Новий офер", "reward_pro": 12000, "link": "https://example.com", "is_limited": false, "is_active": true}'
```

## BotFather WebApp домен
У BotFather вкажіть домен для WebApp:
```
localhost
```
Для продакшену вкажіть ваш реальний домен.

## Корисні змінні оточення
- `BACKEND_PORT` та `FRONTEND_PORT` для зміни локальних портів.
- `VITE_BACKEND_URL` і `VITE_BOT_USERNAME` для фронтенду.
