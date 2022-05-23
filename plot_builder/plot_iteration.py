

class PlotIteration:
	def __init__(self, _logger, title: str, plot: str, imdb_rating: str, rt_rating: str, genre_rating: str, improvement: str):
		self.title = title
		self.plot = plot
		self.imdb_rating = imdb_rating
		self.rt_rating = rt_rating
		self.genre_rating = genre_rating
		self.improvement = improvement

		_logger.info(self)

	def __repr__(self):
		return f"""
			title       : {self.title}\n
            plot        : {self.plot}\n
            imdb_rating : {self.imdb_rating}\n
			rt_rating   : {self.rt_rating}\n
            genre_rating: {self.genre_rating}\n
            improvement : {self.improvement}\n"""

	def __str__(self):
		return f"""
			title       : {self.title}\n
            plot        : {self.plot}\n
            imdb_rating : {self.imdb_rating}\n
			rt_rating   : {self.rt_rating}\n
            genre_rating: {self.genre_rating}\n
            improvement : {self.improvement}\n"""
