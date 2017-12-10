TOKEN = <TOKEN>
headers = {'Content-Type' : 'application/json' } #get the content in json format
headers["Authorization"] = "token " + TOKEN #authentication for github
GITHUB_API_URL = "https://api.github.com"
orgs = ["/twitter/repos", "/auth0/repos", "/nasa/repos", "/mozilla/repos", "/adobe/repos"]