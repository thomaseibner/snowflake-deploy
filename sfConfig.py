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
        root_config_file = os.path.join(script_dir, filename)
        cur_config_file = os.path.join(cur_dir, filename)
        if (file_exists(root_config_file)):
            config = json.loads(open(str(root_config_file)).read())
        if (file_exists(cur_config_file)):
            # don't overwrite
            tmp_config = json.loads(open(str(cur_config_file)).read())
            for config_key in tmp_config:
                config[config_key] = tmp_config[config_key]
        self.config = config
