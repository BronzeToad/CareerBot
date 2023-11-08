from src.helpers import generate_content as GenCon

# =========================================================================== #

# MODEL = ''
# RESUME_FILENAME = ''
# JOB_DESCRIPTION_FILENAME = ''
# COMPANY_PROFILE_FILENAME = ''

COMPANY = 'Affirm'
POSITION = 'Senior Software Engineer, Backend (Consumer)'

response = GenCon.generate_content_api_call(COMPANY, POSITION)
print(response)