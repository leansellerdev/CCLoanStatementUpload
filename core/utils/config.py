import yaml

from core.utils.logger import Logger

from settings import CONFIG_PATH


class Config:
    def __init__(self) -> None:
        self.config = self._load_config()
        self.logger = Logger(self.__class__.__name__,
                             to_file=False).set_logger()

    @staticmethod
    def _load_config(config_file: str = CONFIG_PATH) -> dict:
        try:
            with open(config_file, 'r', encoding='utf-8') as openfile:
                config = yaml.safe_load(openfile)

                return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file '{config_file}' not found.")
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML file '{config_file}': {exc}")

    def get(self, key: str, default: any = None) -> any:
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> any:
        return self.config[key]
