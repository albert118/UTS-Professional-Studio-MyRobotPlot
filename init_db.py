import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO movies (title, genre, plot, characters, tone, plot_length, iterations) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('First movie', 'Genre for the first movie', 'Plot for the first movie', 'None', 'None', 'None', 'None')
            )

cur.execute("INSERT INTO movies (title, genre, plot, characters, tone, plot_length, iterations) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Second movie', 'Genre for the second movie', 'Plot for the second movie', 'None', 'None', 'None', 'None')
            )

connection.commit()
connection.close()
