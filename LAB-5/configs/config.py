# owasp_a05_lab/app/configs/vulnerable_config.py

# This file is intentionally exposed to demonstrate Sensitive File Exposure.
# In a real application, such secrets would be stored securely (e.g., in environment variables, secret managers).

DATABASE_HOST = "localhost"
DATABASE_USER = "dbuser"
DATABASE_PASSWORD = "super_secret_db_pass_123" # This is a sensitive secret!
API_KEY = "ABC-123-DEF-456-FLAG{EXPOSED_CONFIG_SECRET}" # FLAG embedded here
DEBUG_MODE = True
INTERNAL_NETWORK_RANGE = "192.168.1.0/24"