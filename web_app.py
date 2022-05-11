import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from .app import web_tool
# from .rudalle.image_generator import get_image


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_movie(movie_id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?',
                        (movie_id,)).fetchone()
    conn.close()
    if movie is None:
        abort(404)
    return movie


@app.route('/')
def index():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)


@app.route('/<int:movie_id>')
def movie(movie_id):
    movie = get_movie(movie_id)


    # if os.path.isdir('static/' + movie.title.replace(' ', '_')):
    #     for movie in :
    #         "image_" + i = 1

    return render_template('movie.html', movie=movie)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        user_title = request.form['title']
        genre = request.form['genre']
        characters = request.form['characters']
        tone = request.form['tone']
        plot_length = request.form['plot_length']
        iterations = request.form['iterations']
        args = {"genre": genre, "characters": characters, "tone": tone, "plot_length": plot_length, "iterations": int(iterations)}
        title, plot, imdb_rating, rt_rating = web_tool(args)
        if user_title == '':
            title = title
        else:
            title = user_title

        # image_option=False
        # if image_option == True:
        #     get_image(plot, title)
        conn = get_db_connection()
        conn.execute('INSERT INTO movies (title, genre, plot, characters, tone, plot_length, iterations, imdb_rating, '
                     'rt_rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (title, genre, plot, characters, tone, plot_length, iterations, imdb_rating, rt_rating))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    movie = get_movie(id)

    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE movies SET title = ?, genre = ?'
                         ' WHERE id = ?',
                         (title, genre, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    movie = get_movie(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM movies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(movie['title']))
    return redirect(url_for('index'))

