# Konzeption einer Webanwendung zur Einreichung und veröffentlichung von Arzneimittel-Lieferengpässen in der Bundesrepuplik Deutschland


# Einführung (Thematisch)


# Einleitung (Technisch)

In diesem Repository werden Sie einige Werkzeuge bereitgestellt bekommen mit denen Sie arbeiten können.

## Werkzeuge

### Virtual Box
Um mit dem User der virtuellen Maschine auf freigegebende Verzeichnisse des Hosts zuzugreifen, muss der User in der zu bestehenden Gruppe aufgenommen werden. Vorher müssen die Guest Additions installiert worden sein.

Folgender Befehl im Terminal:

`sudo adduser tristan vboxsf`

### Docker
Für die Installation von Docker installiere ich zunächst curl.

`apt-get install curl`

Im Anschluss kann Docker direkt von der Docker-Homepage gezogen und installiert werden.

`curl https://get.docker.com | bash`

Damit für die Verwendung von Docker nicht jedes Mal root herhalten muss, nehme ich den lokalen User tristan in die entsprechende Gruppe für Docker auf.

`sudo usermod -aG docker tristan`

Für einen ersten Test muss die Maschine neu gestartet oder eine Ab/Anmeldung durchgeführt werden. Nun ziehe ich einen Container ohne root Rechte und nehme diesen in Betrieb.

`docker run --detach --restart always --name portainer --publish 9000:9000 --volume /var/run/docker.sock:/var/run/docker.sock portainer/portainer`

### Docker - Regisrty

Docker bietet eine komfortable Lösung Services in ressourcenschonenden Containern zu erstellen, zu betreiben und zu versionieren.

Dafür muss `Docker` zunächst auf Ihrem Arbeitsplatz installiert werden. Auf die Installation von Docker verzichten wir gerne an der Stelle und verweisen auf http://www.docker.io.

Eine der schönen Eigenschaften von Docker ist, dass es auf allen Betriebssystemen zur Verfügung steht. Somit können die folgendenden Mittel unabhängig vom Betriebssystem gerne genutzt werden.
Für eine bequeme Handhabe bei der weiteren Entwicklung und Administration, haben wir mit `portainer` (http://portainer.io) gearbeitet. Dies bietet eine Web-GUI und kann gleich in einem ersten Schritt als Docker-Container gezogen und betrieben werden.

```bash
docker run --detach --restart always --name portainer --publish 9000:9000 --volume /var/run/docker.sock:/var/run/docker.sock portainer/portainer

```

Portainer bietet die Möglichkeit Docker-Images, -Container, -Volumes und weitere Funktionen auf dem lokal installerten Docker-Sockel zu verwalten. Unter die noch nicht genannten Funktionen fällt auch die Verwaltung der lokalen Docker-Registry sowie die Versionierung und Ablage der Docker-Images. Wahlweise kann auch eine Verbindung zu anderen Registries aufgebaut werden, um Images zu pullen oder zu pushen.

Unser Dockerverzeichnis enthält:

```bash
-- docker/
	-> _data/
	-> README.md

```

Zur Trennung der von uns parallel abgearbeiteten Arbeitsergebnisse und zentralen Zusammenführung der dabei entstandenen Image-Versionen, haben wir in diesem Verzeichnis das Volume eines `Docker-Registry-Containers` abgelegt. Die Implementierung eines Volume-Mountpionts und die Versionierung der Docker-Registry mit den erarbeiteten Images stellen sicher, dass keine Arbeitsergebnisse verloren gehen.

```bash
docker run --detach --restart always --name registry --publish 5000:5000 --volume /media/sf_Desktop/MeinFlask/docker/_data:/var/lib/registry registry:2

```

### Flask - Webapp

Erstellung des Dockerimages:

```bash
docker build -t dockerfile/demo .

```

Aufbau einer Lauffähigen temporären Umgebung in einem DockerKontainer mit Mount der Projektdaten:

```bash
docker run -p 4444:5000 -it --rm -v /media/sf_Desktop/lieferengpassflask/_data:/root/flaskproj dockerfile/demo

```

Aufbau einer Lauffähigen temporären Umgebung in einem DockerKontainer:

```bash
docker run -p 4444:5000 -it --rm dockerfile/demo

```

### Gitlab

```bash
docker run --detach     --hostname localhost     --publish 443:443 --publish 80:80 --publish 22:22     --name gitlab     --restart always     --volume /srv/gitlab/config:/etc/gitlab     --volume /srv/gitlab/logs:/var/log/gitlab     --volume /srv/gitlab/data:/var/opt/gitlab     gitlab/gitlab-ce:latest

```


# Gruppenmitglieder

* Tristan Klose (Bundesinstitut für Arzneimittel und Medizinprodukte)
* David Schenk (ACT-Gruppe)

Hausarbeit und Gruppenprojekt im Studienfach Webprogrammierung
