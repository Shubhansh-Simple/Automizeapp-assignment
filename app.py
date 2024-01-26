from flask            import Flask
from flask_migrate    import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.config['DEBUG'] = True

# To see all the configuration of current flask app
#print('Yeah Config names - ',app.config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from views import *

if __name__ == '__main__':
    app.run(port=8080)
