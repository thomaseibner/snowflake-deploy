import json
import os

def file_exists(file_path):
    return os.path.exists(file_path)

class SfConfig():

    def __init__(self, filename):
        script_dir = os.path.dirname(__file__)
        cur_dir    = os.getcwd()

        config = {}
        
        # Create initial configuration from the script_dir
        if (file_exists(script_dir + '/' + filename)):
            config = json.loads(open(str(script_dir + '/' + filename)).read())
        if (file_exists(cur_dir + '/' + filename)):
            # don't overwrite
            tmp_config = json.loads(open(str(cur_dir + '/' + filename)).read())
            for config_key in tmp_config:
                config[config_key] = tmp_config[config_key]
        self.config = config
