import os
import sys

sys.path.insert(0, os.getcwd())

from restdemo import create_app, db

# Create an application instance that web servers can use. We store it as
# "application" (the wsgi default) and also the much shorter and convenient
# "app".

application = create_app(config_name='production')

with application.app_context():
    db.create_all()
    application.logger.info('Initialized the database!')
