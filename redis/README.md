# Redis database

This [Redis image](https://hub.docker.com/_/redis) will serve as the messaging queue for this application. Messages will be added to the queue each time an update is made to the **Trip Planner Postgres SQL Database**.

To deploy and access Redis on Kubernetes, execute the following terminal commands:

```bash
kubectl apply -f redis/deployment.yaml

kubectl apply -f redis/service.yaml
```

These commands will configure a Kubernetes pod to host Redis, and a Load Balancer service so that the Redis pod may be access either by service name (from within Kubernetes cluster) or externally (via **EXTERNAL_IP**).