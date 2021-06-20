# mflambda


### Create a python 3.9 virtual env named venv

```
cp caching_urllib.py venv/lib/python3.9/site-packages/
cp config.ini venv/lib/python3.9/site-packages/
cp lambda_function.py venv/lib/python3.9/site-packages/
cp table_extractor.py venv/lib/python3.9/site-packages/
cp table_formatter.py venv/lib/python3.9/site-packages/
cp util.py venv/lib/python3.9/site-packages/
```

### Move to site-packages and zip the contents to create a `lambda_function.zip`
`cd venv/lib/python3.9/site-packages`

`zip -r9 ../../../../lambda_function.zip * -x diskcache/\* -x diskcache-4.1.0.dist-info/\*`

