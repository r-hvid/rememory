from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from datetime import datetime, timedelta
from app import db
from app.main import bp
from app.models import Category, Topic, Answer
from app.main.forms import AnswerForm, CategoryForm, TopicForm
from markdown import markdown

@bp.route('/', methods=['GET', 'POST'])
def index():
    categories = Category.query.all()

    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(
            title=form.title.data,
            description=form.description.data
        )

        db.session.add(category)
        db.session.commit()

        flash("The category {} was added".format(category.title))

        return redirect(url_for('main.index'))

    return render_template('index.html', categories=categories, add_category_form=form)


@bp.route('/category/<int:id>', methods=['GET', 'POST'])
def category(id):
    category = Category.query.get_or_404(id)

    form = TopicForm()

    if form.validate_on_submit():
        topic = Topic(
            title=form.title.data,
            body=form.body.data,
            body_html=markdown(form.body.data),
            category_id=category.id
        )

        db.session.add(topic)
        db.session.commit()

        flash("The topic {} was to added to category {}".format(topic.title, category.title))

        return redirect(url_for('main.category', id=id))

    return render_template('category.html', category=category, add_topic_form=form)


@bp.route('/topic/<int:id>', methods=['GET', 'POST'])
def topic(id):
    current_topic = Topic.query.get_or_404(id)

    form = TopicForm()

    if form.validate_on_submit():
        sub_topic = Topic(
            title=form.title.data,
            body=form.body.data,
            body_html=markdown(form.body.data),
            category=current_topic.category,
            parent=current_topic
        )

        db.session.add(sub_topic)
        db.session.commit()

        flash("Sub-topic {} was added to topic {}".format(sub_topic.title, current_topic.title))

        return redirect(url_for('main.topic', id=id))

    return render_template('topic.html', topic=current_topic, add_child_topic_form=form)


@bp.route('/review')
def review():
    topics = Topic.query.all()

    topics.sort(key=lambda current_topic: current_topic.waiting_progress, reverse=True)

    return render_template('review.html', topics=topics[:25])


@bp.route('/review/<int:id>', methods=['GET', 'POST'])
def review_topic(id):
    topic = Topic.query.get_or_404(id)

    form = AnswerForm()

    if form.validate_on_submit():
        topic.update_topic(form.performance_rating.data)

        answer = Answer(
            topic=topic,
            body=form.body.data,
            body_html=markdown(form.body.data)
        )

        db.session.add(answer)
        db.session.commit()
        flash("You answered the topic {} and gave yourself the performance rating {}".format(
            topic.title, answer.performance_rating)
        )

        return redirect(url_for('main.answer', id=answer.id))

    return render_template('review_topic.html', topic=topic, answer_form=form)


@bp.route('/answer/<int:id>', methods=['GET', 'POST'])
def answer(id):
    answer = Answer.query.get_or_404(id)

    form = AnswerForm()

    if form.validate_on_submit():
        answer.performance_rating = form.performance_rating.data
        db.session.commit()

        return redirect(url_for('main.review'))

    return render_template('answer.html', answer=answer, form=form)