from src.helpers import generate_content as GenCon

# =========================================================================== #

# MODEL = ''
# RESUME_FILENAME = ''
# JOB_DESCRIPTION_FILENAME = ''
# COMPANY_PROFILE_FILENAME = ''

COMPANY = ''
POSITION = ''

response = GenCon.generate_content_api_call(COMPANY, POSITION)
print(response)