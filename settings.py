from pathlib import Path


DEBUG = True

PATH = Path(__file__).resolve().parent

CONFIG_PATH = PATH / 'config.yaml'
ENV_PATH = PATH / 'secrets.env'
LOG_FILE_PATH = PATH / 'app.log'

nca_layer_path = r"C:\Users\96514502\AppData\Roaming\NCALayer\NCALayer.exe"
