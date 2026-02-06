# Telegram Web App Casino Ecosystem

Повний стек для Telegram WebApp + бот + бекенд.

## Вимоги
- Docker та Docker Compose.

### Як встановити Docker
- Windows/Mac: завантажте Docker Desktop з офіційного сайту https://www.docker.com/ і встановіть.
- Linux: використайте інструкцію для вашого дистрибутиву на сайті Docker.

## Запуск
1. Скопіюйте `.env.example` у `.env` та заповніть значення (домен `blacktime.uno`, бот `casino_prof_bot`).
2. Переконайтесь, що DNS домену вказує на ваш сервер і відкривається у браузері.
3. Запустіть сервіси:
   ```bash
   docker compose up -d --build
   ```
4. Отримайте SSL-сертифікат:
   ```bash
   docker compose run --rm certbot
   ```
5. Перезапустіть nginx:
   ```bash
   docker compose restart nginx
   ```

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
- Nginx:
  ```bash
  docker compose logs -f nginx
  ```

Також логи пишуться у папку `logs/`.

## Додавання каналів і оферів через curl
### Додати канал
```bash
curl -X POST https://blacktime.uno/admin/channels \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: 8578805679" \
  -d '{"channel_id": -1001234567890, "link": "https://t.me/channel", "title": "Супер канал", "is_required": true}'
```

### Додати офер
```bash
curl -X POST https://blacktime.uno/admin/offers \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: 8578805679" \
  -d '{"title": "Новий офер", "reward_pro": 12000, "link": "https://example.com", "is_limited": false, "is_active": true}'
```

## BotFather WebApp домен
У BotFather вкажіть домен для WebApp:
```
blacktime.uno
```
Для відкриття WebApp у Telegram потрібен HTTPS-домен і він має бути доданий у BotFather.

## Корисні змінні оточення
- `DOMAIN` і `CERTBOT_EMAIL` для SSL.
- `CORS_ORIGINS` та `WEBAPP_URL` повинні дорівнювати `https://blacktime.uno`.
- `VITE_BACKEND_URL` і `VITE_BOT_USERNAME` для фронтенду.
