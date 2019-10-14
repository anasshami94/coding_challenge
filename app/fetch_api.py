import requests
import config
import json
class MergedApi:
    def __init__(self, **args):
        self.key = args.get('key')
        self.user = args.get('user')
        self.repo = args.get('repo')
        self.team_name = args.get('team_name')
        self.err = None
        self.data = None 
    
    def _json_request(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return json.loads(response.content)
        except Exception:
            pass
        return {}
    def _recersive_request(self, url, data=[]):
        try:
            response = requests.get(url)
            subdata = response.json()
            data = data + subdata['values']
            if 'next' in subdata.keys():
                return self._paging_request(subdata['next'], data)
            else:
                return data
        except Exception:
            pass

        return {}

    def getHighLevelRepoInfo(self):
        if self.repo:
            pass
        else:
            return dict(err='Not Found!', code='404')
    
    def getForkedOriginalCounts(self):
        if self.repo:
            pass
        else:
            return dict(err='Not Found!', code='404')
    
    def getMergedObj(self, git_team, git_repos, bit_repos):
        """
            merge git and bit repos and extract count information
        """
        code = 200
        err = ""
        merged = {}
        languages = {}
        public_count = git_team.get('public_repos', 0)
        followers_count = git_team.get('followers', 0)
        fork_count = 0
        git_keys = ['fork', 'forks_count', 'watchers_count', 'language', 'description']
        bit_keys = ['is_private', 'language', 'description']
        for repo in git_repos:
            repo_data = {}
            for key in git_keys:
                current_val = repo.get(key)

                if not current_val:
                    continue # skip if not found
                if key == 'fork':
                    fork_count += 1
                elif key == 'language':
                    lang = current_val.lower()
                    languages[lang] = languages.get(lang, 0) + 1

            merged[repo['name']] = repo_data

        for repo in bit_repos:
            repo_data = dict()
            if repo['name'] not in merged:
                for key in bit_keys:
                    current_val = repo.get(key)
                    if not current_val:
                        continue # skip if not found
                    if key == 'is_private':
                        public_count += 1
                    else:
                        if key == 'language':
                            lang = current_val.lower()
                            languages[lang] = languages.get(lang, 0) + 1
                try:
                    watchers_href = repo['links']['watchers']['href']
                    repo_data['watchers_count'] = repo_data.get('watchers_count', 0) +\
                                                  self._json_request(watchers_href).get('size',0)
                except KeyError:
                    pass
                merged[repo['name']] = repo_data
        data = {
            'public_repos_count': public_count,
            'followers_count': followers_count,
            'forked_repos_count': fork_count,
            'non_forked_repos_count': public_count - fork_count,
            'list_languages': languages,
            'repos': merged
        }
        merged_data = {
            'data': data,
            'code': code,
            'err': ""
        }
        return merged_data
    def getMergedTeam(self):
        """
        fetch team information from bitbucket and git 
        """
        response_obj = dict(
            data="",
            err="",
            code=200
        )
        git_repos_data = []
        bit_repos_data = []
        GIT_TEAM_URI = config.GITHUB_API_ENDPOINT + "/orgs/{team_name}".format(team_name=self.team_name)
        git_team_info = self._json_request(GIT_TEAM_URI)
        GIT_REPOS_URI = git_team_info.get('repos_url')
        if GIT_REPOS_URI:
            self.repo = GIT_REPOS_URI
            git_repos_data = self._json_request(GIT_REPOS_URI)
        else:
            print('Cant find any information for this team on github') #  you can log some thing here 
            """ or just throw an json error = Not Found
            response_obj.update({
                'code': 404,
                'err': 'Cant find any information for this team on github'
            })
            return response_obj
            """

        # There is a pagination in API. lets do some fix
        BIT_REPOS_URI = config.BITBUCKET_API_ENDPOINT + "/repositories/{team_name}".format(team_name=self.team_name)
        if BIT_REPOS_URI:
            bit_repos_data = self._recersive_request(BIT_REPOS_URI)
        else:
            print('Cant find any information for this team on bitbucket') #  you can log some thing here
            """ or just throw an json error = Not Found
            response_obj.update({
                'code': 404,
                'err': 'Cant find any information for this team on bitbucket'
            })
            return response_obj
            """
        merged_data = self.getMergedObj(git_team_info, git_repos_data, bit_repos_data)
        response_obj.update (merged_data)

        return response_obj
        
