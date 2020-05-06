import os
os.environ["CACHE_REQUESTS"] = "1"

from lambda_function import LambdaHandler

LambdaHandler('local_tester', None)



