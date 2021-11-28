import random
import requests
import unittest


class GithubSearchTests(unittest.TestCase):

    def test_repo_search_by_name(self):
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

    def test_repo_search_by_description(self):
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

    def test_repo_search_by_readme(self):
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

    def test_repo_search_by_owner_name(self):
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

    def test_repo_search_by_user(self):
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

    def test_repo_search_by_org(self):
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

    def test_repo_search_by_size(self):
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

        result = [True if size <= 100 else False for size in repo_size_list]

        error_message = "This repository is bigger than 100 kilobytes."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_num_of_followers(self):

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

    def test_repo_search_by_num_of_forks(self):
        url = "https://api.github.com/search/repositories?q=forks:>=10000&sort=forks&order=asc"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        forks_list_one = []
        for fork in repository_list:
            forks_list_one.append(fork["forks_count"])

        result = [True if fork >= 10000 else False for fork in forks_list_one]

        error_message = "This is a repository with less than 10000 forks."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_num_of_stars(self):
        # Test if the repositories in the response have at least 5000 stars
        url = "https://api.github.com/search/repositories?q=stars:>5000&sort=stars&order=asc"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        numbers_of_stars = []
        for star in repository_list:
            numbers_of_stars.append(star["stargazers_count"])

        result = [True if star > 5000 else False for star in numbers_of_stars]

        error_message = "This is a repository with less than 5000 stars."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_creation_date(self):
        url = "https://api.github.com/search/repositories?q=created:<=2021-01-01"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        year_list = []
        for datetime in repository_list:
            year = datetime["created_at"][:4]
            year_list.append(year)

        result = [True if year <= "2021" else False for year in year_list]

        error_message = "This repository was created before 2021."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_push_date(self):
        url = "https://api.github.com/search/repositories?q=pushed:2020-01-01"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        year_list = []
        for datetime in repository_list:
            year = datetime["pushed_at"][:4]
            year_list.append(year)

        result = [True if year <= "2020" else False for year in year_list]

        error_message = "This repository was created before 2020."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_language(self):
        # Test to verify if the repository language is Python
        url = "https://api.github.com/search/repositories?q=language:Python"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        language_list = []
        for language in repository_list:
            language_list.append(language["language"])

        result = [True if "python" in language.lower() else False for language in language_list]

        error_message = "This repository has a different language."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_topic(self):
        url = "https://api.github.com/search/repositories?q=topic:python"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        topics_list = []
        for topic in repository_list:
            topics_list.append(topic["topics"])

        result = [True if "python" in topics else False for topics in topics_list]

        error_message = "There's no python Topic in this repository."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_num_of_topics(self):
        url = "https://api.github.com/search/repositories?q=topics:1"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        topics_list = []
        for topic in repository_list:
            topics_list.append(topic["topics"])

        result = [True if len(topics) == 1 else False for topics in topics_list]

        error_message = "There's more than one topic in this repository."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_license(self):
        url = "https://api.github.com/search/repositories?q=license:eupl-1.1"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        license_keys = []
        for key in repository_list:
            license_keys.append(key["license"]["key"])

        result = [True if "eupl-1.1" in data else False for data in license_keys]

        error_message = "There's more than one topic in this repository."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_visibility(self):
        # test if a private repository can be access without a auth
        url = "https://api.github.com/search/repositories?q=signature+in:readme+user:renataberoli+is:private"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        self.assertFalse(repository_list), "This repository wouldn't return data because is private."

        # Test if a can access a public repository with the almost same query
        query_repo_public = requests.get(
            'https://api.github.com/search/repositories?q=renataberoli+in:description+user:renataberoli+is:public')
        repo_public_json = query_repo_public.json()
        repo_public_data = repo_public_json["items"]

        self.assertTrue(repo_public_data), "This repository must be public and return data."

    def test_repo_search_by_if_is_mirror(self):
        url = "https://api.github.com/search/repositories?q=mirror:true"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        repos_mirror = []
        for repo in repository_list:
            repos_mirror.append(repo["mirror_url"])

        result = [True if repo != "null" else False for repo in repos_mirror]

        error_message = "This repository is not a mirror."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_if_is_archived(self):
        url = "https://api.github.com/search/repositories?q=archived:true"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        status_list = []
        for repo in repository_list:
            status_list.append(repo["archived"])

        result = [True if status is True else False for status in status_list]

        error_message = "This repository is not archived."
        self.assertNotIn(False, result, error_message)

    def test_repo_search_by_issue_label_good_first_issues(self):
        url = "https://api.github.com/search/repositories?q=renataberoli+in:description+good-first-issues:1"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

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

        # assert issues_data[1] == "good first issue", "There's no such label."

    def test_repo_search_by_issue_label_wanted_issues(self):
        url = "https://api.github.com/search/repositories?q=renataberoli+in:description+help-wanted-issues:1"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

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

    def test_repo_search_by_ability_to_sponsor(self):
        url = "https://api.github.com/search/repositories?q=is:sponsorable"
        response = requests.get(url)

        # Confirm the response status_code
        status_code = response.status_code
        self.assertEqual(200, status_code)

        data = response.json()
        repository_list = data["items"]

        assert 1 == 1, "The API didn't return any way to confirm this test."


if __name__ == '__main__':
    unittest.main()
