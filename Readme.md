# EK 1041 Datenmanagement Distributed Data Structures

Autor: **Benjamin Popesku, Sebastian Profous**
Version: **15-04-26**

## Detalierte Aufgabenstellung

Recherchieren Sie mögliche Werkzeuge für das "distributed Computing". Vergleichen Sie mögliche Produkte in Bezug auf folgende Parameter:

Architektur
einsetzbare Programmiersprachen
Datenverteilung und gemeinsamer Speicher
Performance bei Main-Focus
Notifikation von Master oder anderen Slaves
Um Technologien auch entsprechend im Einsatz vergleichen zu können, ist die Beschreibung der Schnittstellen ein wichtiger Punkt. Hierfür bietet sich auch eine kurze Sourcecode Gegenüberstellung an, damit die Komplexität des Systems bzw. Frameworks auch veranschaulicht werden kann.

Nehmen Sie eine geeignete Aufgabenstellung/Berechnung (Aufteilung von Daten) und zeigen Sie anhand von einer Beispiel-Konfiguration, wie die Verteilung der Berechnung und anschließende Zusammenführung der Daten funktioniert. Bei ähnlichen oder gleichen Berechnungen wäre ein direkter Vergleich (Benchmark) der gewählten Tools/Technologien von Vorteil.

## Recherche 

### Was wollen wir erreichen?

Wir versuchen rechenintensive Aufgaben auf mehrere "Rechner/Worker" aufzuteilen damit diese ihre Aufgabe erfüllen und sie dann später wieder zu einem
ganzen zusammengefügt werden können. Hier konzentrieren wir uns des weiteren auf die Möglichkeiten die hier verglichenen Tools auch gescheit
in einer Cloud zu deployen und auch dort sinnvol zu betreiben.

## Apache Spark

Apache Spark arbeitet, wer hätte es sich nur denken können, mit einen Chef (hier der sogenannte Driver) welcher einen DAG (Directed Acyclic Graph)
für die geplante Arbeit erstellt, arbeiten annimt und an die verschiedenen Workern (hier die sogenannten Executoren) verteilt.

Wenn das ganze in einer Cloud Umgebung deployed werden sollte übernimmt ein sogenannter Cluster Manager wie Kubernetes oder Yarn die Verteilung
der Ressourcen. Spark teilt hierbei seine Daten auf verschiedene Partitionen auf welche dann an die Worker weitergereicht werden. Jede kleine
Transformation fürht zu der Erstellung eines neuen RDDs (Resilient Distributed Dataset) was dann bei der nächsten "Aktion" wirklich berrechnet wird.

### Cloud

Ein eigenes Clouddeployment ist für Apache Spark ziemlich einfach. Die meisten Cloudanbieter beiten Spark meist bereits als verwalteten Service 
an. Es ist also nicht viel schwerer als eine App zu installieren.

So kann Spark zum Beispiel auf AWS über das sogennante Amazon EMR (Elastic MapReduce) deployed werden. Über dieses Tool wird automatisch
eine vodefinierte Workeranzahl erstellt, einfaches Patching/Monitoring ermöglicht und es kann ein Automatisches Skalling eingestellt werden um
einfach auf verschiedene Auslastungen reagieren zu können. Alternativ kann Sparks auch einfach mithilfe von Kubernetes gehosted werden.

Auch die Google Cloud/Azure ermöglichen eine ähnlich einfache integratien eines Spark Sevices.

Aber wenn man - wie die meisten von uns - beschließen sollte das ganze über Container auf seinen eigenen Kubernetes Cluster zu Deployen bietet Spark nun seit Version 2.3 einen eigenen nativen Kubernetes Mode an:

Yaml file fürs Spark depl:

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sparky
data:
  SPARK_MASTER_URL: "placeholder"
  SPARK_NAMESPACE: "sparky"
  SPARK_EXECUTOR_INSTANCES: "4"
  SPARK_EXECUTOR_MEMORY: "2g"
  SPARK_EXECUTOR_CORES: "2"
```

Einrichten von Jobs auf Sparks:

```bash
spark-submit \
  --master placeholder \
  --deploy-mode cluster \
  --name sparky_to_the_moon \
  --conf spark.executor.instances=4 \
  --conf spark.kubernetes.container.image=apache/spark-py:latest \
  --conf spark.kubernetes.namespace=sparky \
  local:///app/master.py
```

Dadurch erstellt Spark ganz viele kleine Worker Pods die die Aufgaben erfüllen aber nach beendigung ihres jobs wieder entfernt werden.
Das bedeutet der Cluster "existiert" nur so lange wie der Job wirklich dauert. 

### Programmiersprachen

Spark unterstützt nativ Python , Java, Scala und R. Scala ist die native Sprache des Frameworks und sorgt daduch für die beste Performance. PySpark ist dafür aber am weitesten verbreitet.

### Datenverteilung / Shared Storage

Spark verwendet das sogenannte In-Memory_Computing. Das bedeutet das versucht wird so viele Daten wie möglich in den RAM der verschiedenen
Worker zu speichern. In der CLoudumgebung wird dafür ein Objekt Store verwendet - zB S3 auf AWS. Spark liest dann alle Daten aus den Objekt
Store aus, verarbeitet sie im Memory und liefert die Ergebnisse zurück. Das bedeutet aber auch das Shuffles - also die Datenverteilung
zwischen verschiedenen Exekutoren auf das absolute Minimum reduziert werden sollten.

### Performance

Die Größte Stärke ist wie bereits gesagt die Batch verarbeitung im Ram. Für die meisten iterativen Algorithmen ist Sparks dadurch
deutlich schneller als seine Konkurrenten die auf die Disk zugreifen. Über das Structured Streaming ist sogar eine Echtzeitverarbeitung
möglich - diese kommt jedoch mit hohen latenzen. 

### Notifications

Eine eigene Worker to Worker kommunikation gibt es bei Sparks nicht. Auch die Kommunikation zwischen Master-Worker ist nicht so ausgeprägt
wie bei anderen Systemen. Der Driver beobachtet passiv den Status der Arbeiten über den Cluster-Manager und kann so arbeiten umverteilen/vergeben.

## Celery/Redis



## Ray




## Durchgeführte Arbeitsschritte


## Quellen