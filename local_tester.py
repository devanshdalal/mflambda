import os
os.environ["CACHE_REQUESTS"] = "1"

from lambda_function import LambdaHandler

LambdaHandler({'resources': ['arn:aws:events:ap-south-1:733082014204:rule/scheduled-weekly-3']},
	None)



