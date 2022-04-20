import sqlite3

class NetflixDAO:

    def __init__(self, path: str) -> None:
        """Path to the database needs to be submitted when creating dao object"""
        self.path = path

    def get_movie_by_title(self, title: str) -> dict:
        """Get most recent movie with the given title"""
        with sqlite3.connect(self.path) as connection:
            # Query results from the database
            cursor = connection.cursor()
            sql_query = f"""
                    SELECT title, country, release_year, description
                    FROM netflix
                    WHERE title = '{title}'
                    ORDER BY release_year DESC
            """
            cursor.execute(sql_query)
            query_result = cursor.fetchone()
            # Make a dictionary with the query results
            pretty_result = {
                'title': query_result[0],
                'country': query_result[1],
                'release_year': query_result[2],
                'description': query_result[3],
            }
        return pretty_result

# Start app
if __name__ == '__main__':
    from config import DB_NETFLIX
    db = NetflixDAO(DB_NETFLIX)
    print(db.get_movie_by_title('A Good Wife'))
