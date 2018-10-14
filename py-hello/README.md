# gcloud function with python (Python 3.7 Runtime)

### Note:

Demo with the beta python support in cloud functions

The cloud function name matches the name of the function we defined in code: py_hello

- Cloud Functions file naming

Your function's entrypoint must be contained in a Python source file named _main.py_.

- Specifying dependencies

Dependencies in Python are managed with pip and expressed in a metadata file called _requirements.txt_ shipped alongside your function. This file must be in the same directory as the _main.py_ file that contains your function code.


## Prerequisites

- gloud cli tool
- python 3.7

- gcloud account

## Deploying

```
gcloud functions deploy py_hello --runtime python37 --trigger-http --entry-point=main_function
```

- Trigger: We are going to go with the HTTP Trigger since we want to invoke it directly via a HTTPs endpoint. This creats a unique URL.

