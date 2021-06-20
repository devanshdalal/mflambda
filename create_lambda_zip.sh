#!/bin/bash

rm -f lambda_function.zip

cp caching_urllib.py venv/lib/python3.9/site-packages/
cp config.ini venv/lib/python3.9/site-packages/
cp lambda_function.py venv/lib/python3.9/site-packages/
cp table_extractor.py venv/lib/python3.9/site-packages/
cp table_formatter.py venv/lib/python3.9/site-packages/
cp util.py venv/lib/python3.9/site-packages/



cd venv/lib/python3.9/site-packages

zip -r9 ../../../../lambda_function.zip * -x diskcache/\* -x diskcache-4.1.0.dist-info/\* -x \*__pycache__\*
