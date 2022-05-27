DROP TABLE IF EXISTS movies;

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    plot TEXT NOT NULL,
    characters TEXT NOT NULL,
    tone TEXT NOT NULL,
    plot_length INTEGER NOT NULL,
    iterations INTEGER NOT NULL,
    imdb_rating TEXT NOT NULL,
    rt_rating TEXT NOT NULL
);
