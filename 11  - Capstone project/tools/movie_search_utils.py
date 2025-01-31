import omdb
import os


class ImdbMovieLinkFetcher:
    """
    Class for fetching IMDb links using by movie name.
    """

    def __init__(self):
        self.client = omdb.OMDBClient(apikey=os.getenv("OMDB_API_KEY"))

    def get_imdb_link(self, movie_title):
        """
        Query the OMDb API with the given movie title and return the IMDb link.
        Returns None if the movie wasn't found or if an error occurred.

        :param movie_title: The title of the movie (string)
        :return: The IMDb link (string) or None
        """

        data = self.client.search_movie(movie_title)
        imdb_id = data[0].get("imdb_id")
        if imdb_id:
            return f"https://www.imdb.com/title/{imdb_id}/"
