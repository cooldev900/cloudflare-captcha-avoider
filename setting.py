from environs import Env

env = Env()
env.read_env()

SMS_ACTIVATE_API_KEY = env.str('SMS_ACTIVATE_API_KEY')

HAPPN_URL = env.str('HAPPN_URL')
