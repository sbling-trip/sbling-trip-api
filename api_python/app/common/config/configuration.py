import logging
import logging.config
import os
from configparser import NoSectionError, ConfigParser


class Configuration:
    """
    Singleton 클래스
    """
    _instance = None
    config: ConfigParser

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            phase = os.getenv("PHASE", "local")
            cls._instance.config = ConfigParser()
            # unit test 환경에서도 파일을 잘 찾을 수 있도록 __file__과 상대경로를 이용
            current_file_directory = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.abspath(f"{current_file_directory}/../../../resources/config-{phase}.ini")
            cls._instance.config.read(config_file)
            # logging_config_file = os.path.abspath(
            #     f"{current_file_directory}/../../resources/logging/logging-{phase}.ini"
            # )
            # logging.config.fileConfig(logging_config_file, disable_existing_loggers=False)
            logging.info(f"Loaded config from: {config_file}")

        return cls._instance

    def get(self, section: str, key: str):
        return self.config.get(section, key)

    def __getitem__(self, key):
        # configparser 내부 코드를 보면 section이 없을때 subscript로 요청 시 KeyError, get으로 요청시에는 NoSectionError가 발생함
        # Python의 __getitem__ 문서를 보면 key가 없을 때 KeyError를 발생시켜야 한다고 되어있지만
        # 이 경우 NoSectionError가 발생하는 것이 더 일관성이 있기때문에 NoSectionError가 발생하도록 함
        try:
            return self.config[key]
        except KeyError:
            raise NoSectionError(key)


config = Configuration()
