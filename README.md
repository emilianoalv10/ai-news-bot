# 🤖 AI News Bot

Bot que recopila las últimas novedades sobre AI de fuentes gratuitas y genera un resumen diario usando Claude.

## Fuentes (todas gratis, sin API keys)

- 🔍 **Google News RSS** - Noticias de AI de medios globales
- 💬 **Reddit** - r/artificial, r/MachineLearning, r/ChatGPT, r/LocalLLaMA, r/singularity
- 🟧 **Hacker News** - Posts trending sobre AI

## Setup

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar API key

```bash
cp .env.example .env
```

Solo necesitás la **Anthropic API Key** (para que Claude genere el resumen):
- Obtener en [console.anthropic.com](https://console.anthropic.com)

### 3. Ejecutar

```bash
# Una sola vez
python main.py

# Modo programado (todos los días a las 09:00 UTC)
python main.py --schedule
```

## Output

El resumen incluye:
- 🔥 Trending del día
- 📰 Novedades por categoría
- 🏆 Posts más destacados con links
- 📊 Tendencias generales

Los resúmenes se guardan en `summaries/summary_YYYY-MM-DD.md`

## Configuración

Editar `config.py` para ajustar queries, subreddits, umbrales de score, etc.
