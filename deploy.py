#!/usr/bin/env python3

import json
import os
from os import walk
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

    deploy_config = os.path.join(cur_dir, 'deploy.json')
    if (file_exists(deploy_config) == False):
        print(f"No deploy.json file found in {cur_dir}")
        exit(2)
    deploy_order = json.loads(open(str(deploy_config)).read())    

    print("Deploying scripts ...")
    for file in deploy_order:
        if (file[0] != '@'):
            # Should we allow multiple statements in a single file?
            print(f"Deploying {file} ...", end='')
            if (file_exists(os.path.join(cur_dir, file))):
                file_contents = open(str(os.path.join(cur_dir, file))).read()
                cursor = sf_conn.run_query(file_contents)
                print(" done")
                print()
                for res_sth in cursor:
                    res_str = ','.join([str(x) for x in res_sth])
                    print(res_str)
                cursor.close()
            else:
                print("not found!")
        else:
            # Deploy objects in directory following @ into the stage
            stage = file
            directory = file[1:]
            print(f"Deploying files to the stage {stage}")
            if (file_exists(directory) == False):
                print(f"Directory {directory} does not exist")
                break
            for r, d, f in os.walk(directory):
                # remove the directory from the path 
                upload_dir = r[(len(directory)):]
                for stg_file in f:
                    print(f"Uploading file {stg_file} to {file}{upload_dir} ", end='')
                    cursor = sf_conn.run_query(f"PUT file://{os.path.join(cur_dir, r, stg_file)} {file}{upload_dir} AUTO_COMPRESS = FALSE OVERWRITE = TRUE")
                    print (" done")
                    for res_sth in cursor:
                        res_str = ','.join([str(x) for x in res_sth])
                        print(res_str)
                    cursor.close()
                
    sf_conn.close_conn()

if __name__ == "__main__":
    main()
