from environs import Env

env = Env()
env.read_env()

SMS_ACTIVATE_API_URL = 'https://api.yescaptcha.com/createTask'

HAPPN_URL = env.str('HAPPN_URL')
