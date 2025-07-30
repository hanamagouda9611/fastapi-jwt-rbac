import secrets

secret_key = secrets.token_urlsafe(32)
print("Your SECRET_KEY is:", secret_key)

#  python -c "import secrets; print(secrets.token_urlsafe(32))"