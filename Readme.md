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

Auch Celery arbeitet, wer hätte es gedacht, mit einen "Master" und einen "Worker" - auch wenn diese ein wenig anders funktionieren als bei Spark. So legt der Master (hier der sogenannte Producer)
eine von ihm erzeugte Task in eine Queu (hier der sogenannte Broker). Die verschiedenen Worker hollen sich aus der Que eine Task für sich hinaus die sie dann bearbeiten. In diesen Fall 
wird Redis als Broker und Result Store verwendet. Die gesammte Architektur ist deutlich "leichter" als Spark und auf einen Task bassierten betrieb ausgelegt.

### Claud

Genauso wie Spark ist Celery bei den meisten gängigen Cloudanbietern sehr einfach deploybar. Auf AWS kann Celery zum Beispiel über den sogenannten Dienst Amazon ElastiCache for Redis 
betrieben werden. Dabei handelt es sich um einen verwalteten Redis Cluster der mit vielen Features wie zum Beispiel einen automatischen Failover daherkommt. Die Celery Worker werden 
als sogenannte ECS (Elastic Container Service) Tasks oder EKS Pods deployed und können automatisch skalliert werden.

Auf Google geht es ähnlich einfach wobei der Cloud Memorystore for Redis als Broker Backend verwendet wird un die Worker Container auf GKE deployed werden (Google Kubernetes Engine). 
Auf Azure wird der sogenannte Azure Cach for Redis verwendet.

Ein beispielhaftes Deployment mit Kubernetes sieht dann so aus:

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-worker
spec:
  replicas: 4        
  selector:
    matchLabels:
      app: celery-worker
  template:
    metadata:
      labels:
        app: celery-worker
    spec:
      containers:
      - name: worker
        image: your-registry/celery-app:latest
        env:
        - name: CELERY_BROKER_URL
          value: "redis://redis-service:6379/0"
        - name: CELERY_RESULT_BACKEND
          value: "redis://redis-service:6379/0"
        command: ["celery", "-A", "tasks", "worker",
                  "--concurrency=4", "--loglevel=info"]
```

Oder ein deployment wo die Worker je nach der Que länge gestartet werden:

```yml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: celery-worker-scaler
spec:
  scaleTargetRef:
    name: celery-worker
  minReplicaCount: 1
  maxReplicaCount: 20
  triggers:
  - type: redis
    metadata:
      address: redis-service:6379
      listName: celery        
      listLength: "10"        
```

Über dieses Setup skaliert der Clouster automatisch. Wenn zum Beispiel ca 100 in der Que stehen können bis zu 10 Worker erstellt werden.

### Programmiersprache

Bei Celery handelt es sich um ein Python Framework. 

### Datenverteilung

Die Tasks werden über Redis vergeben - was einen gemeinsamen "Speicher" damit am nächsten kommt. Für größere Datensätze erhält der Worker meist nur eine Referenz (zB S3) 
auf die wirklichen Daten die dann direkt asud dem Cloud Storage geladen werden. Redis selbst kann mit größeren Daten nicht umgehen.

### Performance

Celery wurde auf eine große Anzahl von kleinen und unabhängigen Tasks mit niedriger Latenz ausgelegt. Celerys stärken liegen aber in seiner Flexibitität was die Workflow 
Definitionen angeht und die einfache horizontale Skallirbarkeit. Für datenintensive Berechnungne auf große zusammenhängende Datensätze ist Spark deutlich effektiver.

### Notifications

Im Vergleich zu Ray und Spark bietet Celery hier das größte Notificaitonsystem an. Der Master kann synchron auf Ergebnisse der Worker warten, die eigenen Tasks können Callbacks 
auslösen und über Signals werden Worker über Ereignisse (Task started, Task Error, etc) informiert. Mit Chord wird zum Beispiel ein Callback ausgelöst wenn alle parallelen Tasks 
einer Gruppe erfüllt wurden.

## Ray

Bei Ray handelt es sich um ein natives Python Framework für verteilte Systeme welches in erster Linie für KI und Maschinelearningworkflows ausgelegt wurde. Es gibt, oh wunder, 
auch hier wieder eine "Master" (eine sogenannte Head Note), welcher den globalen Zustand verwaltet, und kleine Worker Nodes welche die Aufgaben ausführen. Die Metadaten werden 
in einen Global Control Store gespeichert welcher gleichzeitig auch den Cluster koordiniert. Besonders dabei ist aber das Ray zwischen Tasks (zustandslose Funktionen) und 
Actors (zustandsbehaftete Objekte auf denen ein Worker existiert) unterscheidet.

Ray wurde von Anfang an auf für ein Kubernetes Deployment konzipiert. KubeRay ist der offizielle Kubernetes-Operator für Ray:

```yml
apiVersion: ray.io/v1alpha1
kind: RayCluster
metadata:
  name: prime-cluster
spec:
  rayVersion: '2.9.0'
  headGroupSpec:
    rayStartParams:
      dashboard-host: '0.0.0.0'
    template:
      spec:
        containers:
        - name: ray-head
          image: rayproject/ray:2.9.0
          resources:
            requests:
              cpu: "2"
              memory: "4Gi"
            limits:
              cpu: "2"
              memory: "4Gi"
  workerGroupSpecs:
  - replicas: 4               
    minReplicas: 1
    maxReplicas: 10           
    rayStartParams: {}
    template:
      spec:
        containers:
        - name: ray-worker
          image: rayproject/ray:2.9.0
          resources:
            requests:
              cpu: "2"
              memory: "4Gi"
```

Auch hier wurde wieder ein Auto Scalling eingerichtet.

### Cloud

Auch wie die anderen Lösungen lässt sich Ray sehr einfach auf den gängigen Cloudanbietern deployen. Amazon bietet auf AWS über den sogenannten Amazon SageMaker nativen Ray 
support für Maschinelearning Workflows. Auf Google Cloud läuft Ray auf GKE mit KubeRay, und Vertex AI unterstützt Ray ebenfalls nativ. Auf Azure wird Ray auf AKS mit KubeRay deployt. 

### Programmiersprache

Obwohl Ray ein natives Python Framework ist gibt es auch eine Java SDK.

### Datenverteilung

Für jede Note besitzt Ray einen einzigartigen Objekt Store (zB Apache Plasma) der einen wirklichen gemeinsamen Speicher zwischen Tasks auf derselben Node ermöglicht. Sollte 
ein Task auf einer anderen Node zugriff auf etwas aus diser Node brauchen wird dies über das Netzwerk übertragen und dort gecached - also ein Distributed Objekt Store.

### Performance

Ray wurde auf AI/ML Workloads optimiert. Also heterogene Tasks mit einer niedrigen Latenz. Über den Shared Object Store ist der Overhead pro Task aufruf minimal. Die Funktionen 
RayTune (Hyperparameteroptimierung - was für n Wort), RayTrain (verteiltes ML Training) und RayServe (Model serving) machen Ray zu einer perfekten Plattform für AI Anwendungen. 
Für reine Datengeschichten ist Spark noch immer deutlich effektiver.

### Notifications

Ray arbeitet mit sogenannten ObjektRefs (Futures) für die Kommunikation. Jede Task gibt sofort einen ObjektRef wieder auf den der Master wartet. Über die verwendung von Actors 
können Worker direkt miteinander inteagieren - zum Beispiel eine Methode eines anderen Workers aufrufen. Dadurch wird eine Worker to Worker Kommunikation hergestellt.

## Durchgeführte Arbeitsschritte


## Quellen