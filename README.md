# README

## Setting up virtual env

```bash
  apt install python3.10-venv
  source virt_env/bin/activate
```

- create requirement file
`pip freeze > requirement.txt`

- downloading packages and libraries 
`pip install -r requirement.txt`

- Use this to ignore gRPC warnings
`export GRPC_VERBOSITY=ERROR`