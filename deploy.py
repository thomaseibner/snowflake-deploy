#!/usr/bin/env python3

import json
import os
from sfConn import SfConn
from sfConfig import SfConfig

script_dir = os.path.dirname(__file__)
cur_dir    = os.getcwd()

#print(f"Script location: {script_dir}\nCWD: {cur_dir}");

def file_exists(file_path):
    return os.path.exists(file_path)

def main():
    # Replace the above with a library to
    cfg = SfConfig('config.json')
    sf_conn = SfConn(cfg.config)
    sf_conn.verify_conn()

    deploy_config = None
    if (file_exists(cur_dir + '/deploy.json')):
        deploy_config = cur_dir + '/deploy.json'
    else:
        print(f"No deploy.json file found in {cur_dir}")
        exit(2)
    deploy_order = json.loads(open(str(deploy_config)).read())    

    print("Deploying scripts ...")
    for file in deploy_order:
        print(f"Deploying {file} ...", end='')
        if (file_exists(cur_dir + '/' + file)):
            file_contents = open(str(cur_dir + '/' + file)).read()
            cursor = sf_conn.run_query(file_contents)
            print(" done")
            print()
            for res_sth in cursor:
                res_str = ','.join([str(x) for x in res_sth])
                print(res_str)
            cursor.close()
        else:
            print("not found!")

    sf_conn.close_conn()

if __name__ == "__main__":
    main()
