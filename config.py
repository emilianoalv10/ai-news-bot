"""Configuration for the AI News Bot."""

# Google News RSS search queries
GOOGLE_NEWS_QUERIES = [
    "artificial intelligence",
    "AI breakthrough",
    "ChatGPT Claude Gemini GPT",
    "OpenAI Anthropic Google AI",
    "large language model LLM",
    "generative AI",
    "AI regulation policy",
]

# Reddit subreddits to scan
SUBREDDITS = [
    "artificial",
    "MachineLearning",
    "ChatGPT",
    "LocalLLaMA",
    "singularity",
]

# Minimum Reddit score to include a post
MIN_REDDIT_SCORE = 50

# Max items per source
MAX_PER_SOURCE = 30

# Total max items to send to the summarizer
MAX_ITEMS_FOR_SUMMARY = 80
