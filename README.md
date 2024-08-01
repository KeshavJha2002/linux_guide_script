# README

## Setting up virtual env

```bash
  apt install python3.10-venv
  python3 -m venv virt_env
  source virt_env/bin/activate
```

- create requirement file

`pip freeze > requirement.txt`

- downloading packages and libraries 

`pip install -r requirement.txt`

- Use this to ignore gRPC warnings

`export GRPC_VERBOSITY=ERROR`

- To make the script avalaible globally

`sudo cp -r cli_buddy.sh usr/local/bin`

- To link the cli_buddy.sh -> cli_buddy

`sudo ln -s /usr/local/bin/cli_buddy.sh /usr/local/bin/cli_buddy`