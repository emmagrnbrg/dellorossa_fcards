LOGIN_PATTERN = r"^[a-zA-Z][a-zA-Z0-9_]{7,31}$"  # маска для валидации логина пользователя
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # маска для валидации адреса эл. почты пользователя

OPERATION_LIFETIME_MIN = 15  # время жизни пользовательских операций в минутах

ACCESS_TOKEN_LIFETIME_MINUTES = 15  # время жизни access-токена в минутах
REFRESH_TOKEN_LIFETIME_MINUTES = 43200  # время жизни refresh-токена в минутах (30 дней)
