# webdev-project

Für die Vorlesung in Web Programmierung sollen wir eine App entwickeln   
Wir haben uns für eine Arzneimittel-Lieferengpass App entschieden   
     
     
## Was kann die App?
    
* Bereitstellen von Informationen über Arzneimittel-Lieferengpässe in Deutschland    
* Hersteller von Arzneimittel pflegen die Daten über ihren Arzneimittelbestand   
* Stakeholder die diesen Informationen benötigen werden darüber informiert
* Arzneimittel werden in zwei Klassen kategoriersiert
    

## requirements

### MongoDB 3.2.12
    
```bash
$  sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
$  echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
$  sudo apt-get update
$  sudo apt-get install -y mongodb-org
```

#### Erstellen einer Unit file zum steuern der MongoDB (Ubuntu 16.04)  
    
```bash
$  sudo nano /etc/systemd/system/mongodb.service
```

Inhalt der mongodb.service
```bash
[Unit]
Description=High-performance, schema-free document-oriented database
After=network.target

[Service]
User=mongodb
ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf

[Install]
WantedBy=multi-user.target
```

```bash
$  sudo systemctl start mongodb
$  sudo systemctl enable mongodb
```
    
### virtualenv
     
```bash
$  virtualenv -p $(which python3) venv
$  source venv/bin/activate
```

### pip (python dependencies)
     
```bash
$  pip install -r requirements.txt
```

### Umgebungsvariablen
   
```bash
$  export SECRET_KEY="<secret-key>"
$  export mongo_ip="<mongodb-ip>"
```
    

## tech stack
    
* Python 3
* MongoDB (NoSQL Datenbank)
* MongoEngine
* Flask Micro-Framework
* Jinja2 TemplateEngine
* Flask-Login
* WTForms
* Werkzeug Security
* Semantic-UI
* jQuery
