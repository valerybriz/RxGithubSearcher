import os

TOKEN = os.getenv("GITHUB_API_TOKEN", "<TOKEN>")
GITHUB_API_URL = "https://api.github.com"

headers = {"Content-Type": "application/json" }
headers["Authorization"] = "token " + TOKEN
orgs = [
    "/twitter/repos",
    "/auth0/repos",
    "/nasa/repos",
    "/mozilla/repos",
    "/adobe/repos",
]
