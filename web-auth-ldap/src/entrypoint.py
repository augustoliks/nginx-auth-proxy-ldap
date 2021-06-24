import os

import controllers
import conf

conf.set_log_level(os.getenv('LOG_LEVEL', 'DEBUG').upper())

# for wsgi app server
app = controllers.create_app()


if __name__ == '__main__':
    # for cli
    app.run()
