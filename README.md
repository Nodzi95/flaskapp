# flaskapp

implementováno (Flask framework) a testováno s Python 3.7.4 ve VSCode (Windows)

# Spuštění:

a) inicializace databáze (dropne staré tabulky a vytvoří nové), aplikace by si měla sama databázi vytvořit, pokud ji nenajde - databáze dostupná v souboru myproject/deso.sqlite:

  python myproject/db_init.py
  
b) spuštění aplikace:

  python run.py
  
  nebo nastavením env. proměnné:
  
  (BASH) export FLASK_APP="myproject" | (PowerShell) $env:FLASK_APP = "myproject" | (CMD) set FLASK_APP="myproject"
  
  a spustit:
  
  flask run

c) testování

  unit testy dostupné v myproject/test_app.py


# Poznámky:

server využívá vytváření (os.makedirs) a mazání záložek (shutil)

GUI vytvořeno převážně z komponent https://getbootstrap.com/
