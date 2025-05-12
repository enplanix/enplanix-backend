import os
import dotenv

ENV_FILE=os.getenv('ENV_FILE', '.env.dev')

dotenv.load_dotenv(f'./{ENV_FILE}')
settings_mode = os.getenv('PROJECT_SETTINGS', 'local')

if settings_mode == 'local':
    from .local import *
elif settings_mode == 'prod':
    from .prod import *
else:
    raise ValueError("Unknown settings module.")
