from flask import Flask, g      

from flask import (render_template, flash, redirect, url_for, abort)
from flask.wrappers import Response

from flask_bcrypt import check_password_hash

from flask_login import (LoginManager, login_user, logout_user,
                        login_required, current_user)


DEBUG = True
app = Flask(__name__)
app.secret_key = "786sd32rj289fgkm5yh780bgf65rfp;asdpo'4390['56o[rtxl[k54sd765o[er76t69tp7qw3r74y98jhjt"

@app.route('/')
@app.route('/entries')
def index():
    return render_template("index.html")

@app.route('/entries/new')
def create():
    return render_template("new.html")

@app.route('/entries/<id>')
def detail(id):
    return render_template('detail.html')

@app.route('/entries/<id>/edit')
def edit(id):
    return render_template('edit.html')

@app.route('/entries/<id>/delete')
def delete(id):
    flash("the deleted command has been called!")
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug=DEBUG)
