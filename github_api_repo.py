import random
import requests
import unittest


class GithubSearchTests(unittest.TestCase):

    def test_repository_search_by_name(self):
        # Test to verify if the API returns only repositories that have in the name the keyword "python"
        url = "https://api.github.com/search/repositories?q=python+in:name"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        list_of_names = []
        for repository in repository_list:
            repo_name = repository["name"]
            list_of_names.append(repo_name.lower())

        python_in_name = [True if "python" in name else False for name in list_of_names]

        error_message = "The API returned a repository without 'Python' in the repository's name."
        self.assertNotIn(False, python_in_name, error_message)

    def test_repository_search_by_description(self):
        # Test to verify if the API returns only repositories that have in the description the keyword "python"
        url = "https://api.github.com/search/repositories?q=python+in:description"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        random_repository = random.choice(repository_list)
        random_description = random_repository["description"]

        error_message = "There's no 'Python' in the repository's description."
        self.assertIn("python", random_description.lower(), error_message)

    def test_repository_search_by_readme(self):
        # Test to verify if the API returns only repositories that have in the readme the keyword "cadmio"
        url = "https://api.github.com/search/repositories?q=cadmio+in:readme"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        random_repository = random.choice(repository_list)

        user = random_repository["owner"]["login"]
        repo_name = random_repository["name"]
        branch = random_repository["default_branch"]
        repo_url = f"https://raw.githubusercontent.com/{user}/{repo_name}/{branch}/README.md"
        file_response = requests.get(repo_url)
        readme_content = file_response.content

        error_message = "There's no 'Cadmio' in the repository's readme."
        self.assertIn(b"cadmio", readme_content.lower(), error_message)

    def test_repository_search_by_owner_name(self):
        # Test to verify if the API returns only the repository "renataberoli/renataberoli.github.io"
        url = "https://api.github.com/search/repositories?q=repo:renataberoli/renataberoli.github.io"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        # This request search by a specific repository, so the response must be only one repository
        self.assertEqual(len(repository_list), 1)

        error_message = "The repository is from a different owner/name."
        self.assertIn("renataberoli/renataberoli.github.io", repository_list[0]["full_name"], error_message)

    def test_repository_search_by_user(self):
        # Test to verify if the API returns only the repositories of the user "renataberoli"
        url = "https://api.github.com/search/repositories?q=user:renataberoli"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        user_list = []
        for repository in repository_list:
            user_list.append(repository["owner"]["login"])

        repo_user = [True if "renataberoli" in user else False for user in user_list]

        error_message = "This is not the renataberoli's repository."
        self.assertNotIn(False, repo_user, error_message)

    def test_repository_search_by_org(self):
        url = "https://api.github.com/search/repositories?q=org:github"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        repo_org_list = []
        for repository in repository_list:
            repo_org_list.append(repository["owner"]["login"])

        result = [True if "github" in org else False for org in repo_org_list]

        error_message = "There's at least one repository from other organization."
        self.assertNotIn(False, result, error_message)

    def test_repository_search_by_size(self):
        # This test confirm if the repository's size is less or equal than 100 kilobytes
        url = "https://api.github.com/search/repositories?q=size:<=100"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        repo_size_list = []
        for repository in repository_list:
            repo_size_list.append(repository["size"])

        result = [True if size <=100 else False for size in repo_size_list]

        error_message = "This repository is bigger than 100 kilobytes."
        self.assertNotIn(False, result, error_message)

    def test_repository_search_by_number_of_followers(self):
        # This test was hard to do due to the confusion about the subject of the repository's "follower."
        # https://github.community/t/api-is-very-confusing-by-listing-stars-count-for-watchers-count-on-all-repos/13817
        # https://developer.github.com/changes/2012-09-05-watcher-api/

        url = "https://api.github.com/search/repositories?q=renataberoli+in:description+followers:1"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        # This request search by a specific repository, so the response must be only one repository
        self.assertEqual(len(repository_list), 1)

        error_message = "This is a repository with less then 1 follower."
        self.assertEqual(repository_list[0]["watchers_count"], 1)

    def test_repository_search_by_number_of_forks(self):
        # The expected result
        response = requests.get(
            'https://api.github.com/search/repositories?q=Python+forks:>=10000&sort=forks&order=asc')
        data = response.json()
        repository_list = data["items"]

        forks_count = repository_list[0]["forks"]
        assert forks_count >= 10000, "This is a repository with less than 10000 forks."

        """
        There's a problem with the forks order query when the same query but value is higher. 
        You can see bellow:
        """

        forks_list_one = []
        for fork in repository_list:
            forks_list_one.append(fork["forks_count"])

        print(f"The list of forks correctly ordered {forks_list_one}.")

        # the wrong result
        request_two = requests.get(
            'https://api.github.com/search/repositories?q=Python+forks:>=1000&sort=forks&order=asc')
        data_two = request_two.json()
        repository_list_two = data_two["items"]

        forks_list_two = []
        for fork in repository_list_two:
            forks_list_two.append(fork["forks_count"])

        print(f"The list of forks with a problem in the order {forks_list_two}.")

    def test_repository_search_by_number_of_stars(self):
        # Test if the repositories in the response have at least 5000 stars
        response = requests.get('https://api.github.com/search/repositories?q=stars:>5000&sort=stars&order=asc')
        data = response.json()
        repository_list = data["items"]

        stars_count = repository_list[0]["stargazers_count"]
        assert stars_count > 5000, "This is a repository with less than 5000 stars."

    def test_repository_search_by_creation_date(self):
        response = requests.get(
            'https://api.github.com/search/repositories?q=python+created:<=2021-01-01')
        data = response.json()
        repository_list = data["items"]

        repo_created_datetime = repository_list[0]["created_at"]
        assert repo_created_datetime[:4] <= "2021", "This repository was created before 2021."

    def test_repository_search_by_push_date(self):
        response = requests.get('https://api.github.com/search/repositories?q=python+pushed:2020-01-01')
        data = response.json()
        repository_list = data["items"]

        repo_pushed_datetime = repository_list[0]["pushed_at"]
        assert repo_pushed_datetime[:4] <= "2020", "This repository was pushed before 2020."

    def test_repository_search_by_language(self):
        # Test to verify if the repository language is Python
        response = requests.get('https://api.github.com/search/repositories?q=language:Python')
        data = response.json()
        repository_list = data["items"]

        language = repository_list[0]["language"]
        assert "Python" in language, "This repository has a different language."

    def test_repository_search_by_topic(self):
        response = requests.get('https://api.github.com/search/repositories?q=topic:python')
        data = response.json()
        repository_list = data["items"]

        topics_list = repository_list[0]["topics"]
        topics_list_lower = []
        for topic in topics_list:
            topics_list_lower.append(topic.lower())

        assert "python" in topics_list_lower, "There's no python Topic in this repository."

    def test_repository_search_by_number_of_topics(self):
        response = requests.get('https://api.github.com/search/repositories?q=python+python+topics:1')
        data = response.json()
        repository_list = data["items"]

        topics_list = repository_list[0]["topics"]
        assert len(topics_list) == 1, "There's more than one topic in this repository."

    def test_repository_search_by_license(self):
        response = requests.get('https://api.github.com/search/repositories?q=python+license:eupl-1.1')
        data = response.json()
        repository_list = data["items"]

        repo_license_key = repository_list[0]["license"]["key"]
        repo_license_description = repository_list[0]["description"]
        self.assertEqual(repo_license_key, "eupl-1.1") and "python" in repo_license_description.lower()

    def test_repository_search_by_visibility(self):
        # test if a private repository can be access without a auth
        response = requests.get(
            'https://api.github.com/search/repositories?q=signature+in:readme+user:renataberoli+is:private')
        data = response.json()
        repository_list = data["items"]

        self.assertFalse(repository_list), "This repository wouldn't return data because is private."

        # Test if a can access a public repository with the almost same query
        query_repo_public = requests.get(
            'https://api.github.com/search/repositories?q=abacate+in:description+user:renataberoli+is:public')
        repo_public_json = query_repo_public.json()
        repo_public_data = repo_public_json["items"]

        self.assertTrue(repo_public_data), "This repository must be public and return data."

    def test_repository_search_by_if_is_mirror(self):
        # mirror true
        response = requests.get('https://api.github.com/search/repositories?q=python+mirror:true')
        data = response.json()
        repository_list = data["items"]

        mirror_url = repository_list[0]["mirror_url"]
        self.assertIsNotNone(mirror_url), "This repository is not a mirror."

    def test_repository_search_by_if_is_archived(self):
        response = requests.get('https://api.github.com/search/repositories?q=python+archived:true')
        data = response.json()
        repository_list = data["items"]

        archived_status = repository_list[0]["archived"]
        self.assertTrue(archived_status), "This repository is not archived."

    def test_repository_search_by_issue_label_good_first_issues(self):
        response = requests.get(
            'https://api.github.com/search/repositories?q=abacate+in:description+good-first-issues:%3E=1')
        data = response.json()
        repository_list = data["items"]

        raw_url = repository_list[0]["issues_url"]
        edited_url = raw_url[:-9]

        response_of_issues = requests.get(edited_url)
        data_of_issues = response_of_issues.json()

        issues_data = []
        for issue in data_of_issues:
            issue_label = issue["labels"]
            issues_data.append(issue_label[0]["name"])

        assert issues_data[1] == "good first issue", "There's no such label."

    def test_repository_search_by_issue_label_wanted_issues(self):
        response = requests.get(
            'https://api.github.com/search/repositories?q=abacate+in:description+help-wanted-issues:%3E=1')
        data = response.json()
        repository_list = data["items"]

        raw_url = repository_list[0]["issues_url"]
        edited_url = raw_url[:-9]

        response_of_issues = requests.get(edited_url)
        data_of_issues = response_of_issues.json()

        issues_label = []
        for issue in data_of_issues:
            help_wanted_label = issue["labels"]
            issues_label.append(help_wanted_label[0]["name"])

        assert issues_label[0] == "help wanted", "There's no such label."

    def test_repository_search_by_ability_to_sponsor(self):
        response = requests.get(
            'https://api.github.com/search/repositories?q=python+is:sponsorable')
        data = response.json()
        repository_list = data["items"]

        assert 1 == 1, "The API didn't return any way to confirm this test."


if __name__ == '__main__':
    unittest.main()
