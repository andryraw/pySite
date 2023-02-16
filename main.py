from app import app, db
from app.models import User, Film, Director, Genre


#@app.shell_context_processors
#def make_shell_context():
#    return {'db': db, 'User': User, 'Film': Film, 'Director': Director, 'Genre': Genre}


if __name__ == '__main__':
    app.run(debug=False)
