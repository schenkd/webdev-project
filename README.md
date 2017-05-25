# webdev-project

Für die Vorlesung in Web Programmierung sollen wir eine App entwickeln   
Wir haben uns für eine Arzneimittel-Lieferengpass App entschieden   
     
     
## Was kann die App?
    
* Bereitstellen von Informationen über Arzneimittel-Lieferengpässe in Deutschland    
* Hersteller von Arzneimittel pflegen die Daten über ihren Arzneimittelbestand   
* Stakeholder die diesen Informationen benötigen werden darüber informiert
* Arzneimittel werden in zwei Klassen kategoriersiert

### virtualenv
     
```bash
$  virtualenv -p $(which python3) venv
$  source venv/bin/activate
```

### pip requirements
     
```bash
$  pip install -r requirements.txt
```

## tech stack
    
* Python 3
* MongoDB NoSQL
* MongoEngine
* Flask Micro-Framework
* Jinja2 TemplateEngine
* Flask-Login
* WTForms
* Werkzeug Security
* Semantic-UI
* jQuery
