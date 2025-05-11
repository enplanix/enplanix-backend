import os
import dotenv

dotenv.load_dotenv('./.env.dev')
settings_mode = os.getenv('PROJECT_SETTINGS', 'local')

if settings_mode == 'local':
    from .local import *
elif settings_mode == 'prod':
    from .prod import *
else:
    raise ValueError("Unknown settings module.")
