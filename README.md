# snowflake-deploy

## Overview

Simple python-based framework for quickly deploying code or objects during development to Snowflake.

## Table of Contents

1. [Overview](#overview)
1. [Setup](#setup)
1. [Dependencies](#dependencies)
1. [Future Enhancements](#future-enhancements)
1. [Author](#author)
1. [License](#license)

## Setup

`mkdir ~/.snowflake`

Follow the guide on [Key Pair Auth @ Snowflake.com](https://docs.snowflake.com/en/user-guide/key-pair-auth.html#step-1-generate-the-private-key) to create a `rsa_key.p8` private key and an `rsa_key.pub` public key to assign the user in Snowflake.

Alter your user in Snowflake to set the rsa_public_key to the key in `rsa_key.pub`

Place the private key in your `~/.snowflake/` directory and ensure it is only readable by yourself (`chmod 600 rsa_key.p8`)

This code assumes your key isn't encrypted by default so no passphrase is required. You can decide to have your key passphrase as an environment variable to unlock the key with or alter the `sfConn.py` class to accept the passphrase as an input.

To setup the deployments you create a `config.json` containing your connection parameters in your main directory containing the `sfConfig.py, sfConn.py, and deploy.py` script:

```
{
    "account"   : "<YOUR_SNOWFLAKE_ACCOUNT>",
    "user"      : "your@login",
    "warehouse" : "DEMO_WH",
    "role"      : "DEMO_ROLE",
    "database"  : "DEMO_DB",
    "schema"    : "PUBLIC"
}
```
You can override individual options by placing a `config.json` file in each directory to reflect the database/schema/roles required for deploying objects. Sample override of a single schema inheriting the remaining configuration from the file above:
```
{
    "schema"    : "DEMO_SC"
}
```
What to deploy is defined in the `deploy.json` file in each directory you have. It is set up similar to the configuration file, but instead using an array to force the order of files being applied:
```
[
    "my_stored_proc.drop",
    "my_stored_proc.pr",
    "my_stored_proc.test1"
]
```
As you can see you can execute any single statement and the script will deploy and retrieve the output of any statement executed, which allows you to run a test or populate data immediately after installing an object. 

Now you can run the deploy.py script in the directory with your files:

```
thomas@dl360p:~/github/snowflake-deploy/demo_db.demo_sc$ ../deploy.py
Connecting ...
Verifying connection ...
Connected to <YOUR_SNOWFLAKE_ACCOUNT>
Snowflake version: 6.25.0
Role: DEMO_ROLE
DB: DEMO_DB
Schema: DEMO_SC
Warehouse: DEMO_WH
Deploying scripts ...
Deploying my_stored_proc.drop ... done

MY_STORED_PROC successfully dropped.
Deploying my_stored_proc.pr ... done

Function MY_STORED_PROC successfully created.
Deploying my_stored_proc.test ... done

[Started] MY_STORED_PROC
PARAMETERS
MY_PARAMETER: TEST
DRYRUN: 1

DRYRUN
[Finished] MY_STORED_PROC
```

## Dependencies

Python 3.8+ with the Snowflake connector installed

## Future Enhancements

Ability to deploy the required files for a single object, many, or all.

Ability to only upload if timestamp has changed on files compared to last modified date of object in Snowflake.

## Author

Thomas Eibner (@thomaseibner) [twitter](http://twitter.com/thomaseibner) [LinkedIn](https://www.linkedin.com/in/thomaseibner/)

## License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this tool except in compliance with the License. You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
