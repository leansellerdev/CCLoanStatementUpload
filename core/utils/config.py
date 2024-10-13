import yaml

from environs import Env
from core.utils.logger import Logger

from settings import CONFIG_PATH, ENV_PATH
from settings import DEBUG


class Config:
    def __init__(self) -> None:
        if DEBUG:
            self.env = self._load_env()

        self.config = self._load_config()
        self.logger = Logger(self.__class__.__name__,
                             to_file=False).set_logger()

    @staticmethod
    def _load_env(path: str = ENV_PATH) -> dict:
        env: Env = Env()
        try:
            env.read_env(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Environment file '{path}' not found.")

        return dict(
            proxy=dict(
                proxy_login=env('PROXY_LOGIN'),
                proxy_password=env('PROXY_PASSWORD')
            )
        )

    def _load_config(self, config_file: str = CONFIG_PATH) -> dict:
        try:
            with open(config_file, 'r', encoding='utf-8') as openfile:
                config = yaml.safe_load(openfile)
                if DEBUG:
                    config.update(self.env)

                return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file '{config_file}' not found.")
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML file '{config_file}': {exc}")

    def get(self, key: str, default: any = None) -> any:
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> any:
        return self.config[key]
