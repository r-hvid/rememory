from app import db, create_app
from app.models import Category, Topic, Answer

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Category': Category, 'Topic': Topic, 'Answer': Answer}
