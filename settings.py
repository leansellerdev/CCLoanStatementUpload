from pathlib import Path


DEBUG = True

PATH = Path(__file__).resolve().parent

CASE_DIR = Path(r"C:\Users\96514502\Desktop\cases")

CONFIG_PATH = PATH / 'config.yaml'
ENV_PATH = PATH / 'secrets.env'
LOG_FILE_PATH = PATH / 'app.log'
KEY_PATH = PATH / 'nca_key/GOST512_13bd421799c5114a351ac7128a07e349b7f5e388.p12'

nca_layer_path = r"C:\Users\96514502\AppData\Roaming\NCALayer\NCALayer.exe"
open_jdk_path = r"C:\Users\96514502\AppData\Roaming\NCALayer\jre\bin\javaw.exe"
