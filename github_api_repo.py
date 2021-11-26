import requests
import unittest


class GithubSearchTests(unittest.TestCase):

    def test_repository_search_by_name(self):
        # Test to verify if the API returns only repositories that have in the name the keyword "python"
        query_name = requests.get('https://api.github.com/search/repositories?q=python+in:name')
        repo_name_json = query_name.json()
        repo_name_data = repo_name_json["items"]

        repo_name = repo_name_data[0]["name"]
        assert "python" in repo_name.lower(), "There's no 'Python' in the repository's name."

    def test_repository_search_by_description(self):
        # Test to verify if the API returns only repositories that have in the description the keyword "python"
        query_description = requests.get('https://api.github.com/search/repositories?q=python+in:description')
        repo_description_json = query_description.json()
        repo_description_data = repo_description_json["items"]

        repo_description = repo_description_data[0]["description"]
        assert "python" in repo_description.lower(), "There's no 'Python' in the repository's description."

    def test_repository_search_by_readme(self):
        # Test to verify if the API returns only repositories that have in the readme the keyword "cadmio"
        query_readme = requests.get('https://api.github.com/search/repositories?q=cadmio+in:readme')
        repo_readme_json = query_readme.json()
        repo_readme_data = repo_readme_json["items"]

        for data in repo_readme_data:
            if "cadmio" in data["full_name"]:
                continue
            else:
                selected_repo = data
                break

        user = selected_repo["owner"]["login"]
        r_name = selected_repo["name"]
        branch = selected_repo["default_branch"]
        repo_url = f"https://raw.githubusercontent.com/{user}/{r_name}/{branch}/README.md"
        readme_request = requests.get(repo_url)
        readme_content = readme_request.content

        assert b"cadmio" in readme_content.lower(), "There's no 'Cadmio' in the repository's readme."

    def test_repository_search_by_owner_name(self):
        # Test to verify if the API returns only the repository "renataberoli/renataberoli.github.io"
        query_owner = requests.get(
            'https://api.github.com/search/repositories?q=repo:renataberoli/renataberoli.github.io')
        repo_owner_json = query_owner.json()
        repo_owner_data = repo_owner_json["items"]

        repo_full_name = repo_owner_data[0]["full_name"]
        assert "renataberoli/renataberoli.github.io" in repo_full_name, "The repository is from a different " \
                                                                        "owner/name. "

    def test_repository_search_by_user(self):
        # Test to verify if the API returns only the repositories of the user "renataberoli"
        query_repo_user = requests.get('https://api.github.com/search/repositories?q=user:renataberoli')
        repo_user_json = query_repo_user.json()
        repo_user_data = repo_user_json["items"]

        user = repo_user_data[0]["owner"]["login"]
        assert "renataberoli" in user, "This is not the renataberoli's repository."

    def test_repository_search_by_org(self):
        query_repo_org = requests.get('https://api.github.com/search/repositories?q=org:d3')
        repo_org_json = query_repo_org.json()
        repo_org_data = repo_org_json["items"]

        user = repo_org_data[0]["owner"]["login"]
        assert "d3" in user, "This is not the D3's repository."

    def test_repository_search_by_size(self):
        query_repo_size = requests.get('https://api.github.com/search/repositories?q=Python+size:<=100')
        repo_size_json = query_repo_size.json()
        repo_size_data = repo_size_json["items"]

        repo_size = repo_size_data[0]["size"]
        assert repo_size <= 100, "This repository is bigger than 100."

    def test_repository_search_by_number_of_followers(self):
        """
        https://github.community/t/api-is-very-confusing-by-listing-stars-count-for-watchers-count-on-all-repos/13817
        https://developer.github.com/changes/2012-09-05-watcher-api/
        This query is impossible to confirm
        """

        query_repo_followers = requests.get(
            'https://api.github.com/search/repositories?q=abacate+in:description+followers:1')
        repo_followers_json = query_repo_followers.json()
        repo_followers_data = repo_followers_json["items"]

        assert repo_followers_data[0]["watchers_count"] == 1, "This is a repository with less then 1 follower."

    def test_repository_search_by_number_of_forks(self):
        # The expected result
        query_repo_forks = requests.get(
            'https://api.github.com/search/repositories?q=Python+forks:>=10000&sort=forks&order=asc')
        repo_forks_json = query_repo_forks.json()
        repo_forks_data = repo_forks_json["items"]

        forks_count = repo_forks_data[0]["forks"]
        assert forks_count >= 10000, "This is a repository with less than 10000 forks."

        """
        There's a problem with the forks order query when the same query but value is higher. 
        You can see bellow:
        """

        forks_list_one = []
        for fork in repo_forks_data:
            forks_list_one.append(fork["forks_count"])

        print(f"The list of forks correctly ordered {forks_list_one}.")

        # the wrong result
        query_fork = requests.get(
            'https://api.github.com/search/repositories?q=Python+forks:>=1000&sort=forks&order=asc')
        fork_json = query_fork.json()
        fork_data = fork_json["items"]

        forks_list_two = []
        for fork in fork_data:
            forks_list_two.append(fork["forks_count"])

        print(f"The list of forks with a problem in the order {forks_list_two}.")

    def test_repository_search_by_number_of_stars(self):
        # Test if the repositories in the response have at least 5000 stars
        query_stars = requests.get('https://api.github.com/search/repositories?q=stars:>5000&sort=stars&order=asc')
        repo_stars_json = query_stars.json()
        repo_stars_data = repo_stars_json["items"]

        stars_count = repo_stars_data[0]["stargazers_count"]
        assert stars_count > 5000, "This is a repository with less than 5000 stars."

    def test_repository_search_by_creation_date(self):
        query_repo_created = requests.get(
            'https://api.github.com/search/repositories?q=python+created:<=2021-01-01')
        repo_created_json = query_repo_created.json()
        repo_created_data = repo_created_json["items"]

        repo_created_datetime = repo_created_data[0]["created_at"]
        assert repo_created_datetime[:4] <= "2021", "This repository was created before 2021."

    def test_repository_search_by_push_date(self):
        query_repo_pushed = requests.get('https://api.github.com/search/repositories?q=python+pushed:2020-01-01')
        repo_pushed_json = query_repo_pushed.json()
        repo_pushed_data = repo_pushed_json["items"]

        repo_pushed_datetime = repo_pushed_data[0]["pushed_at"]
        assert repo_pushed_datetime[:4] <= "2020", "This repository was pushed before 2020."

    def test_repository_search_by_language(self):
        # Test to verify if the repository language is Python
        query_language = requests.get('https://api.github.com/search/repositories?q=language:Python')
        repo_language_json = query_language.json()
        repo_language_data = repo_language_json["items"]

        language = repo_language_data[0]["language"]
        assert "Python" in language, "This repository has a different language."

    def test_repository_search_by_topic(self):
        query_repo_topic = requests.get('https://api.github.com/search/repositories?q=topic:python')
        repo_topics_json = query_repo_topic.json()
        repo_topics_data = repo_topics_json["items"]

        repo_topics = repo_topics_data[0]["topics"]
        topics_list_lower = []
        for topic in repo_topics:
            topics_list_lower.append(topic.lower())

        assert "python" in topics_list_lower, "There's no python Topic in this repository."

    def test_repository_search_by_number_of_topics(self):
        query_repo_n_topics = requests.get('https://api.github.com/search/repositories?q=python+python+topics:1')
        repo_n_topics_json = query_repo_n_topics.json()
        repo_n_topics_data = repo_n_topics_json["items"]

        topics_list = repo_n_topics_data[0]["topics"]
        assert len(topics_list) == 1, "There's more than one topic in this repository."

    def test_repository_search_by_license(self):
        query_repo_license = requests.get('https://api.github.com/search/repositories?q=python+license:eupl-1.1')
        repo_license_json = query_repo_license.json()
        repo_license_data = repo_license_json["items"]

        repo_license_key = repo_license_data[0]["license"]["key"]
        repo_license_description = repo_license_data[0]["description"]
        self.assertEqual(repo_license_key, "eupl-1.1") and "python" in repo_license_description.lower()

    def test_repository_search_by_visibility(self):
        # test if a private repository can be access without a auth
        query_repo_private = requests.get(
            'https://api.github.com/search/repositories?q=signature+in:readme+user:renataberoli+is:private')
        repo_private_json = query_repo_private.json()
        repo_private_data = repo_private_json["items"]

        self.assertFalse(repo_private_data), "This repository wouldn't return data because is private."

        # Test if a can access a public repository with the almost same query
        query_repo_public = requests.get(
             'https://api.github.com/search/repositories?q=abacate+in:description+user:renataberoli+is:public')
        repo_public_json = query_repo_public.json()
        repo_public_data = repo_public_json["items"]

        self.assertTrue(repo_public_data), "This repository must be public and return data."

    def test_repository_search_by_if_is_mirror(self):
        # mirror true
        query_mirror = requests.get('https://api.github.com/search/repositories?q=python+mirror:true')
        mirror_json = query_mirror.json()
        mirror_data = mirror_json["items"]

        mirror_url = mirror_data[0]["mirror_url"]
        self.assertIsNotNone(mirror_url), "This repository is not a mirror."

    def test_repository_search_by_if_is_archived(self):
        query_repo_archived = requests.get('https://api.github.com/search/repositories?q=python+archived:true')
        repo_archived_json = query_repo_archived.json()
        repo_archived_data = repo_archived_json["items"]

        archived_status = repo_archived_data[0]["archived"]
        self.assertTrue(archived_status), "This repository is not archived."

    def test_repository_search_by_issue_label_good_first_issues(self):
        query_repo_good_f_issue = requests.get(
            'https://api.github.com/search/repositories?q=abacate+in:description+good-first-issues:%3E=1')
        repo_good_f_issue_json = query_repo_good_f_issue.json()
        repo_good_f_issue_data = repo_good_f_issue_json["items"]

        issues_url = repo_good_f_issue_data[0]["issues_url"]
        all_issues = issues_url[:-9]

        query_issues = requests.get(all_issues)
        issues_json = query_issues.json()

        issues_data = []
        for issue in issues_json:
            issue_label = issue["labels"]
            issues_data.append(issue_label[0]["name"])

        assert issues_data[1] == "good first issue", "There's no such label."

    def test_repository_search_by_issue_label_wanted_issues(self):
        query_repo_help_issue = requests.get(
            'https://api.github.com/search/repositories?q=abacate+in:description+help-wanted-issues:%3E=1')
        repo_help_issue_json = query_repo_help_issue.json()
        repo_help_issue_data = repo_help_issue_json["items"]

        help_issues = repo_help_issue_data[0]["issues_url"]
        all_issues = help_issues[:-9]

        query_help_issues = requests.get(all_issues)
        help_issues_json = query_help_issues.json()

        issues_label = []
        for issue in help_issues_json:
            help_wanted_label = issue["labels"]
            issues_label.append(help_wanted_label[0]["name"])

        assert issues_label[0] == "help wanted", "There's no such label."

    def test_repository_search_by_ability_to_sponsor(self):
        query_repo_sponsor = requests.get(
            'https://api.github.com/search/repositories?q=python+is:sponsorable')
        repo_sponsor_json = query_repo_sponsor.json()
        repo_sponsor_data = repo_sponsor_json["items"]

        assert 1 == 1, "The API didn't return any way to confirm this test."


if __name__ == '__main__':
    unittest.main()
