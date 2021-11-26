import requests
import unittest


class GithubSearchTests(unittest.TestCase):

    def test_user_search_by_followers(self):
        # Test if the user's followers are until 30 followers
        # This test is originally from users with at least 1k followers, but the github api only returns 30
        query_users_followers = requests.get(
            'https://api.github.com/search/users?q=python+followers:%3E=30&sort=followers&order=asc')
        users_followers_json = query_users_followers.json()
        response_users_data = users_followers_json["items"]

        followers_url = response_users_data[0]["followers_url"]
        followers = requests.get(followers_url)
        followers_response = followers.json()

        followers_count = len(followers_response)
        assert followers_count == 30, "This user have more than 30 followers"

    def test_user_search_by_type(self):
        # Test if the user's type is 'Organization'
        query_users_type = requests.get('https://api.github.com/search/users?q=type:org')
        users_type_json = query_users_type.json()
        users_type_data = users_type_json["items"]

        user_type = users_type_data[0]["type"]
        assert user_type == "Organization", "This user's type is User"

    def test_user_search_by_language(self):
        # Test if the user there are at least one repository with the python language
        query_users_language = requests.get(
            'https://api.github.com/search/users?q=language:python+repos:%3E30')
        users_language_json = query_users_language.json()
        users_language_data = users_language_json["items"]

        repos_url = users_language_data[0]["repos_url"]
        user_repos = requests.get(repos_url)
        user_repos_response = user_repos.json()

        repo_language = user_repos_response[2]["language"]
        assert repo_language.lower() == "python", "There's no Python repo in this user account"

    def test_user_search_by_location(self):
        # Test if the location of the user is Denmark
        query_users_location = requests.get('https://api.github.com/search/users?q=python+location:denmark')
        users_location_json = query_users_location.json()
        users_location_data = users_location_json["items"]

        location_url = users_location_data[1]["url"]
        user_location = requests.get(location_url)
        user_location_response = user_location.json()

        location = user_location_response["location"]
        assert location == "Copenhagen, Denmark", "This user is from a different location"


if __name__ == '__main__':
    unittest.main()
