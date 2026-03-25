"""Configuration for the AI News Bot."""

# Twitter search queries for AI news
SEARCH_QUERIES = [
    "artificial intelligence news",
    "AI breakthrough",
    "ChatGPT OR Claude OR Gemini OR GPT",
    "machine learning new",
    "LLM AI",
    "OpenAI OR Anthropic OR Google AI OR Meta AI",
    "AI regulation OR AI policy",
    "generative AI",
]

# Minimum metrics to filter quality tweets
MIN_LIKES = 50
MIN_RETWEETS = 10

# Max tweets to fetch per query
MAX_RESULTS_PER_QUERY = 20

# Total max tweets to send to the summarizer
MAX_TWEETS_FOR_SUMMARY = 100

# Accounts known for AI news (optional priority filter)
PRIORITY_ACCOUNTS = [
    "AndrewYNg",
    "ylecun",
    "kaboroevich",
    "emaborov",
    "sama",
    "demaboris",
    "GoogleAI",
    "OpenAI",
    "AnthropicAI",
    "MetaAI",
    "hardmaru",
    "jackclarkSF",
    "Miles_Brundage",
]
