import yaml
import os


class LoadConf(object):
    @staticmethod
    def config():
        path = os.path.dirname(os.path.abspath(__file__))
        yaml_file = os.path.join(path, "config.yaml")
        file = open(yaml_file, 'r', encoding='utf-8')
        data = yaml.load(file.read(), Loader=yaml.Loader)
        file.close()
        return data
