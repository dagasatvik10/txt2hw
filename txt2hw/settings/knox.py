"""
knox config
"""
from datetime import timedelta

REST_KNOX = {
    "TOKEN_TTL": timedelta(hours=24),
    # "TOKEN_LIMIT_PER_USER": 1,
}
