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

Auch die Google Cloud ermöglicht eine ähnlich einfache integratien eines Spark Sevices über Dataproc.

Auf Google Cloud bietet Dataproc einen vollständig verwalteten Spark-Service. Cluster können in Minuten hochgefahren, nach dem Job wieder gelöscht und über die GCP Console oder Terraform provisioniert werden. Dataproc integriert sich nativ mit Google Cloud Storage (GCS) als Datenspeicher.
Auf Azure heißt der entsprechende Service Azure HDInsight oder – moderner – Azure Databricks, eine auf Spark basierende Analytics-Plattform mit erweiterter UI und MLflow-Integration.
Für ein containerisiertes Deployment auf einem eigenen Kubernetes-Cluster (z.B. EKS, GKE, AKS) bietet Spark seit Version 2.3 einen nativen Kubernetes-Mode:

## Celery/Redis


## Ray




## Durchgeführte Arbeitsschritte


## Quellen