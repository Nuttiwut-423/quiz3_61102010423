from re import template
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.elements import RollbackToSavepointClause
from werkzeug.utils import html

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SECRET_KEY'] = "secret-key"

db = SQLAlchemy(app)

class Book(db.Model):
   title = db.Column(db.String(80),primary_key = True)
   author = db.Column(db.String(80) )
   genre = db.Column(db.String(100))
   height = db.Column(db.Integer())
   publisher = db.Column(db.String(120) )

@app.route('/')
def home():
   return render_template('home.html', books = Book.query.all() )


@app.route('/insert_item', methods = ['GET', 'POST'])
def insert():
    if request.method == 'POST':
      if not request.form['title'] or not request.form['author'] or not request.form['genre']:
         flash('Please enter all the fields', 'error')
      else:

        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        height = request.form['height']
        publisher = request.form['publisher']
          
        book = Book(title=title,author=author,genre=genre,height=height,publisher=publisher)
         
        db.session.add(book)
        db.session.commit()
        flash('successfully')
        return redirect(url_for('home'))
    return render_template('insert.html')


@app.route('/<title>/delete', methods=['GET','POST'])
def delete(title):
    book = Book.query.filter_by(title=title).first()
    if request.method == 'POST':
        if book:
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for('home'))
        abort(404)
 
    return render_template('delete.html')



@app.route('/<title>/update',methods = ['GET','POST'])
def update(title):
    book = Book.query.filter_by(title=title).first()
    if request.method == 'POST' :
        if book:
            db.session.delete(book)
            db.session.commit()

            title = request.form['title']
            author = request.form['author']
            genre = request.form['genre']
            height = request.form['height']
            publisher = request.form['publisher']

            book = Book(title=title,author=author, genre=genre, height=height, publisher=publisher)
 
            db.session.add(book)
            db.session.commit()
            flash('update successfully')
            return redirect(url_for('home'))
        return "ฺBooks with title = {0} Does not match".format(title)
 
    return render_template('update.html', book = book)
