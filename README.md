# 🤖 AI News Bot

Bot que busca las últimas novedades sobre Inteligencia Artificial en Twitter/X y genera un resumen diario usando Claude.

## Features

- 🔍 Busca tweets de AI de las últimas 24hs con múltiples queries
- 📊 Filtra por engagement (likes/retweets) para obtener lo más relevante
- 🧠 Usa Claude (Anthropic) para generar un resumen estructurado en español
- 🔥 Identifica lo trending del día
- 💾 Guarda los resúmenes en archivos markdown
- ⏰ Modo programado para ejecución automática diaria

## Setup

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar API keys

Copiar `.env.example` a `.env` y completar:

```bash
cp .env.example .env
```

Necesitás:
- **Twitter Bearer Token**: Crear app en [Twitter Developer Portal](https://developer.twitter.com)
- **Anthropic API Key**: Obtener en [Anthropic Console](https://console.anthropic.com)

### 3. Ejecutar

```bash
# Una sola vez
python main.py

# Modo programado (se ejecuta todos los días a las 09:00 UTC)
python main.py --schedule
```

## Configuración

Editar `config.py` para ajustar:
- Queries de búsqueda
- Mínimo de likes/retweets
- Cantidad de tweets a analizar
- Cuentas prioritarias

## Output

Los resúmenes se guardan en `summaries/summary_YYYY-MM-DD.md` e incluyen:
- 🔥 Trending del día
- 📰 Resumen de novedades por categoría
- 🧵 Tweets destacados
- 📊 Tendencias generales
