import sqlite3

class NetflixDAO:

    def __init__(self, path: str) -> None:
        """Path to the database needs to be submitted when creating dao object"""
        self.path = path

    def get_title(self, title: str) -> dict:
        """Get most recent movie with the given title

        :param title: Title to search for
        :return: Dictionary with title, country, release year, genre, description
        :raise ValueError: If title not found
        """
        # Query results from the database
        with sqlite3.connect(self.path) as connection:

            cursor = connection.cursor()
            sql_query = f"""
                    SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE title LIKE '%{title}%'
                    ORDER BY release_year DESC
            """
            cursor.execute(sql_query)
            query_result = cursor.fetchone()
        # Make a dictionary with the query results
        if query_result is not None:
            title_found = {
                'title': query_result[0],
                'country': query_result[1],
                'release_year': query_result[2],
                'genre': query_result[3],
                'description': query_result[4],
            }
        else:
            raise ValueError(f'{title} не найден в списке фильмов')
        return title_found

    def get_titles_for_years(self, start_year: int, end_year: int) -> list:
        """Get all up to 100 movies release between years

        :param start_year: Year to start search from
        :param end_year: Year to stop search to
        :return: List of dictionaries with title, release year
        :raise TypeError: If not integers passed as years
        """
        # Check values passed
        if not isinstance(start_year, int) or not isinstance(end_year, int):
            raise TypeError('Values passed as years should be integers')

        else:
            # Query results from the database
            with sqlite3.connect(self.path) as connection:

                cursor = connection.cursor()
                sql_query = f"""
                        SELECT title, release_year
                        FROM netflix
                        WHERE release_year BETWEEN {start_year} AND {end_year}
                        LIMIT 100
                """
                cursor.execute(sql_query)
                query_result = cursor.fetchall()

            # Make a list of dictionaries with the query result
            pretty_result = []
            for title in query_result:
                title_dict = {'title': title[0],
                              'release_year': title[1]
                              }
                pretty_result.append(title_dict)

            return pretty_result

    def get_titles_for_group(self, group: str) -> list:
        """Get titles with the specified ratings

        :param group: only children, family or adult are allowed
        :return: List of dictionaries with title, rating, description
        :raise ValueError: If group passed is not in defined list
        """
        # Ratings for groups
        rating_groups = {
            'children': ('G', 'placeholder'),
            'family': ('G', 'PG', 'PG-13'),
            'adult': ('R', 'NC-17')
        }
        # Check argument passed is in the group list
        if group not in rating_groups.keys():
            raise ValueError(f'Group passed should be one of the following: {rating_groups.keys()}')
        else:
            # Query the database
            allowed_ratings = rating_groups.get(group)
            with sqlite3.connect(self.path) as connection:
                cursor = connection.cursor()
                sql_query = f"""
                        SELECT title, rating, description
                        FROM netflix
                        WHERE rating IN {allowed_ratings}
                """
                cursor.execute(sql_query)
                query_result = cursor.fetchall()

            # Make a list of dictionaries with the query result
            title_list = []
            for title in query_result:
                title_dict = {
                    'title': title[0],
                    'rating': title[1],
                    'description': title[2]
                }
                title_list.append(title_dict)
        return title_list

    def get_titles_for_genre(self, genre: str) -> list:
        """Get most 10 most recent titles for the specified genre

        :param genre: Genre to search titles for
        :return: List of dictionaries with title, description
        """
        # Query the database
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            sql_query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    ORDER BY release_year DESC
                    LIMIT 10
            """
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

        # Prepare list with the query results
        title_list = []
        for title in query_result:
            title_dict = {
                'title': title[0],
                'description': title[1]
            }
            title_list.append(title_dict)
        return title_list

    def get_partners_for_pair(self, *actors: tuple) -> list:
        """Get partners who appeared in more than 2 films with the pair passed

        :param actors: Two actors/actresses for whom to find partners
        :return: List of partners
        """
        # Query the database, get all the partners appeared in the films with the pair
        actor_one, actor_two = actors

        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            sql_query = f"""
                    SELECT "cast"
                    FROM netflix
                    WHERE "cast" LIKE '%{actor_one}%'
                    AND "cast" LIKE '%{actor_two}%'
            """
            cursor.execute(sql_query)
            query_result = cursor.fetchall()

        # Make a dictionary counting number of appearances for each partner
        partners_all = {}
        for group in query_result:
            group = group[0].split(', ')
            for actor in group:
                if actor not in partners_all.keys():
                    partners_all[actor] = 1
                else:
                    partners_all[actor] += 1

        # Make a list with partners appeared in more than 2 films
        partners_result = [partner for partner in partners_all.keys()
                           if partners_all[partner] > 2
                           and partner not in actors]

        return partners_result

    def get_titles(self, type_: str, release_year: int, genre: str) -> list:
        """Get titles for the type, release_year, genre supplied

        :param type: Movie or TV Show
        :param release_year: The year titles were released
        :param genre: Titles genre
        :return: List of dictionaries with title, description
        :raise ValueError: If type passed is not Movie or TV Show
        """
        # Check if type passed is correct
        if type_ not in ('Movie', 'TV Show'):
            raise ValueError(f'Type should be Movie or TV Show, {type_} passed')
        else:
            # Query the database, get the titles meeting conditions
            with sqlite3.connect(self.path) as connection:
                cursor = connection.cursor()
                sql_query = f"""
                        SELECT title, description
                        FROM netflix
                        WHERE type = '{type_}'
                        AND release_year = {release_year}
                        AND listed_in LIKE '%{genre}%'
                """
                cursor.execute(sql_query)
                query_result = cursor.fetchall()

            # Creat resulting list
            titles_list = []
            for title in query_result:
                titles_dict = {
                    'title': title[0],
                    'description': title[1]
                }
                titles_list.append(titles_dict)

        return titles_list
