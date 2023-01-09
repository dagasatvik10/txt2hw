from txt2hw.env import env

AUTH_JWT_COOKIE_KEY = env.str("AUTH_JWT_KEY", "authentication")
AUTH_JWT_COOKIE_SAMESITE = env.str("JWT_AUTH_COOKIE_SAMESITE", default="Lax")
AUTH_JWT_COOKIE_SECURE = env.bool("AUTH_JWT_COOKIE_SECURE", default=False)
