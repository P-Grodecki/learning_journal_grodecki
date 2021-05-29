from datetime import date

from flask import Flask, g      
from flask import (render_template, redirect, url_for)
from flask.globals import request

import models

DEBUG = True
app = Flask(__name__)


@app.before_request
def before_request():
    """ Connect to Database Before each request"""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """ Close connection with database. """
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
def index():
    # Begin stream of journal entries
    if models.Entry.select().count() == 0:
        # If no entries exist, then add a sample entry.
        entry = models.Entry.create_entry(models.sample_entry())    
    entries = models.Entry.select().order_by(models.Entry.entry_date).limit(100)
    return render_template("index.html", entries = entries, models = models)


@app.route('/entries/new', methods=['GET','POST'])
def add():
    # User can add Journal Entries
    if request.method == 'POST':
        form_data = dict(request.form.items())
        new_entry = models.Entry.create_entry(form_data)
        return redirect(url_for('index'))
    return render_template('new.html', thedate = date.today())


@app.route('/entries/<id>', methods=['GET'])
def detail(id):
    # Renders a detail page of the selected journal entry.
    matching_entry = models.Entry.get(entry_id=id)
    return render_template(
        'detail.html', 
        entry = matching_entry,
        long_date_str = models.long_date_str(matching_entry)
        )


@app.route('/entries/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    # Allows user to edit an entry with the id passed into the route.
    # Redirects to the homepage once record is updated.
    matching_entry = models.Entry.get(entry_id=id)
    if request.method == 'POST':
        matching_entry = models.Entry.get(entry_id=id)
        form_data = dict(request.form.items())
        models.update_entry(matching_entry, form_data)
        return redirect(url_for('index'))
    return render_template('edit.html', entry=matching_entry)


@app.route('/entries/<id>/delete')
def delete(id):
    # Deletes the current journal entry and redirects user to homepage.
    delete_row = models.remove_entry(id)
    return redirect(url_for('index'))


if __name__ == "__main__":
    models.initialize()
    if models.Entry.select().count() == 0:
        new_entry = models.Entry.create_entry(models.sample_entry())

    app.run(debug=DEBUG)
