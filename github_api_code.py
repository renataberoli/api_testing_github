import requests
import unittest


class GithubSearchTests(unittest.TestCase):

    def test_search_code(self):
        code_data = requests.get(
            'https://api.github.com/search/code?q=phage+in:file+extension:md+user:voorloopnul')
        code_data_json = code_data.json()
        code_data_response = code_data_json["items"]

        # extension
        filename = code_data_response[0]["name"]
        assert ".md" == filename[-3:], "This file there's not '.md' extension"

        # a word 'phage' in this file
        description = code_data_response[0]["repository"]["description"]
        assert "phage" in description, "There's no 'phage' in the description"


if __name__ == '__main__':
    unittest.main()