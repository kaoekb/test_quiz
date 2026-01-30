Создай папку, склонируй в нее проект \
 `cd tg-quiz-bot`

Переименнуй образец файла с секретом \
`cp .env.example .env`

Запусти сначала докер, затем проект \
`docker compose up --build -d`

Посмотри логи \
`docker compose logs -f`