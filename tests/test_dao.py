import pytest
from dao import NetflixDAO
from config import DB_NETFLIX

class TestNetflixDAO:
    pass

class TestGetTitle(TestNetflixDAO):

    @pytest.mark.parametrize(
        "title, correct_return_type",
        [('Roxy', dict), ('A', dict)]
    )
    def test_search(self, netflix_db, title, correct_return_type):
        query_result = netflix_db.get_title(title)
        return_type = type(query_result)
        assert return_type == correct_return_type, f'Ошибка в возвращаемом типе: ' \
                                                   f'должен быть {correct_return_type}, ' \
                                                   f'возвращается {return_type}'

    def test_keys(self, netflix_db, correct_keys):
        query_result = netflix_db.get_title('A Good Wife')
        keys_to_check = set(query_result.keys())
        assert keys_to_check == correct_keys, f'Ошибка в возвращаемых ключах: должно быть {correct_keys}, ' \
                                              f'возвращается {keys_to_check}'

    def test_type_error(self, netflix_db):
        with pytest.raises(ValueError):
            netflix_db.get_title('title that is not in the database')


class TestGetTitlesForYears(TestNetflixDAO):

    @pytest.mark.parametrize(
        "start_year, end_year, correct_return_type",
        [(2010, 2021, list), (2021, 2010, list)]
    )
    def return_type(self, netflix_db, start_year, end_year, correct_return_type):
        query_result = netflix_db.get_titles_for_years(start_year, end_year)
        return_type = type(query_result)
        assert return_type == correct_return_type, f'Ошибка в возвращаемом типе: ' \
                                                   f'должен быть {correct_return_type}, ' \
                                                   f'возвращается {return_type}'

    def test_type_error(self, netflix_db):
        with pytest.raises(TypeError):
            netflix_db.get_titles_for_years('a', 2010)


class TestGetTitlesForGroup(TestNetflixDAO):

    @pytest.mark.parametrize(
        "group, correct_return_type",
        [('family', list), ('children', list), ('adult', list)]
    )
    def return_type(self, netflix_db, group,correct_return_type):
        query_result = netflix_db.get_titles_for_group(group)
        return_type = type(query_result)
        assert return_type == correct_return_type, f'Ошибка в возвращаемом типе: ' \
                                                   f'должен быть {correct_return_type}, ' \
                                                   f'возвращается {return_type}'

    def test_value_error(self, netflix_db):
        with pytest.raises(ValueError):
            netflix_db.get_titles_for_group('placeholder')

class TestGetTitlesForPair(TestNetflixDAO):

    @pytest.mark.parametrize(
        "first_actor, second_actor, correct_count",
        [('Rose McIver', 'Ben Lamb', 2), ('Jack Black', 'Dustin Hoffman', 2)]
    )
    def test_known_results(self, netflix_db, first_actor, second_actor, correct_count):
        query_result = netflix_db.get_partners_for_pair(first_actor, second_actor)
        results_count = len(query_result)
        assert results_count == correct_count, f"Ошибка в подсчете: должно быть {correct_count}, " \
                                               f"получено {results_count}"


class TestGetTitles(TestNetflixDAO):

    @pytest.mark.parametrize(
        "type_, release_year, genre, correct_return_type",
        [('Movie', 2010, 'drama', list), ('TV Show', 2020, 'comedy', list)]
    )
    def test_known_results(self, netflix_db, type_, release_year, genre, correct_return_type):
        query_result = netflix_db.get_titles(type_, release_year, genre)
        return_type = type(query_result)
        assert return_type == correct_return_type, f'Ошибка в возвращаемом типе: ' \
                                                   f'должен быть {correct_return_type}, ' \
                                                   f'возвращается {return_type}'

    def test_value_error(self, netflix_db):
        with pytest.raises(ValueError):
            netflix_db.get_titles('placeholder', 2010, 'drama')
