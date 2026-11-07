# Speed Codee Backend

Простой API для ИИ (Groq).

## Деплой на Render (бесплатно)

1. Зарегистрируйся на https://render.com
2. New → Web Service
3. Подключи репозиторий или загрузи эти файлы
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. В Environment добавь:
   - `GROQ_API_KEY` = твой ключ
   - `GROQ_MODEL` = `llama-3.3-70b-versatile`

После деплоя скопируй URL (типа `https://xxx.onrender.com`)  
и вставь его в `wispbyte/js/config.js` → `API_URL`  
и поставь `DEMO_MODE: false`

## Локальный запуск

```bash
pip install -r requirements.txt
cp .env.example .env   # заполни ключ
uvicorn app.main:app --reload --port 8000
```
