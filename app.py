# -*- coding: utf-8 -*-
from os import getenv
from os.path import dirname, isfile, join
from dotenv import load_dotenv
from apps import create_app

# a partir do arquivo atual adicione ao path o arquivo .env
_ENV_FILE = join(dirname(__file__), '.env')

# existindo o arquivo faça a leitura do arquivo através da função load_dotenv
if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)


app = create_app(getenv('FLASK_ENV') or 'default')


if __name__ == '__main__':
    ip = '0.0.0.0'
    port = app.config['APP_PORT']
    debug = app.config['DEBUG']

    app.run(host=ip, debug=debug, port=port, use_reloader=debug)
