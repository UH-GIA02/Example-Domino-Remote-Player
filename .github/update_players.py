import json
import os
import base64
from github import Github

def update_players_json(user, repo_link):
    token = os.getenv('DOMINO_PAT')
    g = Github(token)
    repo = g.get_repo("UH-GIA02/Domino-Tournament")
    
    contents = repo.get_contents("src/data/players.json")
    players_data = json.loads(base64.b64decode(contents.content))

    found = False
    for player in players_data:
        if player['github_user'] == user:
            player['repo'] = repo_link  
            found = True
            break
    if not found:
        new_player = {
            "github_user": user,
            "games_played": [],
            "repo": repo_link
        }
        players_data.append(new_player)

    updated_content = base64.b64encode(json.dumps(players_data, indent=4).encode()).decode()

    repo.update_file(contents.path, "Update players.json", updated_content, contents.sha)

if __name__ == "__main__":
    github_user = os.getenv('PR_AUTHOR')
    repo_link = os.getenv('PR_LINK')
    update_players_json(github_user, repo_link)
