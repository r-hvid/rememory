import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    topics = db.relationship('Topic', backref="category", lazy=True)

    def __repr__(self):
        return '<Category: Title: {}>'.format(self.title)


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    answers = db.relationship('Answer', backref="topic", lazy=True)

    parent_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    children = db.relationship("Topic", backref=db.backref('parent', remote_side=[id]))

    difficulty = db.Column(db.Float, default=0.3)
    days_between_reviews = db.Column(db.Float, default=1.0)
    date_last_reviewed = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def update_topic(self, performance_rating):
        waiting_progress = 0

        if performance_rating < 0.6:
            waiting_progress = 1
        else:
            waiting_progress = min(2, (datetime.datetime.utcnow() - self.date_last_reviewed).days/self.days_between_reviews)

        self.difficulty += waiting_progress * 1/17*(8-9*performance_rating)
        
        difficulty_weight = 3 - 1.7 * self.difficulty

        if performance_rating >= 0.6:
            self.days_between_reviews *= 1 + (difficulty_weight) * waiting_progress
        else:
            self.days_between_reviews *= 1 / pow(difficulty_weight,2)
        
        self.date_last_reviewed = datetime.datetime.utcnow()

        db.session.commit()
    
    @hybrid_property
    def waiting_progress(self):
        return min(2, (datetime.datetime.utcnow() - self.date_last_reviewed).days/self.days_between_reviews)
    
    def __repr__(self):
        return '<Topic: Title: {} Body: {}...>'.format(self.title, self.body[:10])


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    performance_rating = db.Column(db.Float)

    def __repr__(self):
        return '<Answer: Topic id: {} Body: {}... Performance: {}>'.format(self.topic_id, self.body[:10], self.performance_rating)