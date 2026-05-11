from github import Github
import json
import base64

# --- KONFIGURÁCIA ---
GITHUB_TOKEN = "tvoj_personal_access_token"
REPO_NAME = "tvoje_meno/tvoj_repozitar"
FILE_PATH = "database.json"  # Cesta k súboru v repozitári

def update_github_db(new_data):
    # 1. Pripojenie k GitHubu
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    
    try:
        # 2. Získanie aktuálneho súboru
        contents = repo.get_contents(FILE_PATH)
        # Dekódovanie obsahu (GitHub posiela base64)
        data = json.loads(base64.b64decode(contents.content).decode('utf-8'))
    except Exception:
        # Ak súbor neexistuje, začneme s prázdnym zoznamom
        data = []
        contents = None

    # 3. Pridanie nových dát
    data.append(new_data)
    
    # 4. Nahranie späť na GitHub (Commit)
    updated_content = json.dumps(data, indent=4)
    
    if contents:
        repo.update_file(
            path=FILE_PATH,
            message="Update databázy cez Python backend",
            content=updated_content,
            sha=contents.sha  # SHA je povinné pre update
        )
    else:
        repo.create_file(
            path=FILE_PATH,
            message="Vytvorenie databázy",
            content=updated_content
        )
    print("Dáta boli úspešne uložené na GitHub!")

# --- TESTOVANIE ---
vstup_od_uzivatela = {"id": 1, "meno": "Peter", "sprava": "Ahoj z Pythonu!"}
update_github_db(vstup_od_uzivatela)
