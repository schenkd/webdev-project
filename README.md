## webdev-project

Für die Vorlesung in Web Programmierung sollen wir eine App entwickeln   
Wir haben uns für eine Arzneimittel-Lieferengpass App entschieden   
     
     
## Was kann die App?
    
* Bereitstellen von Informationen über Arzneimittel-Lieferengpässe in Deutschland    
* Hersteller von Arzneimittel pflegen die Daten über ihren Arzneimittelbestand   
* Stakeholder die diesen Informationen benötigen werden darüber informiert
* Arzneimittel werden in zwei Klassen kategoriersiert

### virtualenv requirements.txt
     
```bash
$  virtualenv -p $(which python3) venv
$  source venv/bin/activate
```

### pip requirements
     
```bash
$  pip install -r requirements.txt
```

## Alternative Installation

Gestartet wird in dem Verzeichnis, in dem das Dockerfile mit dem Gitprojekt liegt.

### Erstellung des Dockerimages:

```bash
$  docker build -t dockerfile/demo .
```

### Aufbau einer Lauffähigen temporären Umgebung in einem DockerKontainer mit Mount der Projektdaten:

```bash
$  docker run -p 4444:5000 -v /Pfad/auf/Hostsystem/_data:/root/flaskproj/ -it --rm dockerfile/demo
```

docker run -p 4444:5000 -v /home/tristan/Dokumente/Webprogrammierung2/Neu/_data:/root/flaskproj/ -it --rm dockerfile/demo

## tech stack
    
* MySQL Database
* Flask Micro-Framework
* Python 3
* SQLAlchemy ORM
