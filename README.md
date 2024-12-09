# Collaborative Trip Planner Service

## Description

## Architecture

### Architecture Diagram

![Database Schema Diagram](images/arch-diagram-final.png)


### Postgres SQL Database Schema

![Database Schema Diagram](images/database-schema.png)

## Deployment to Kubernetes

The Collaborative Trip Planner is designed to be deployed via Kubernetes. The following sequence of terminal commands can be used to deploy all components as a Kubernetes pods:

```bash
kubectl apply -f redis/redis-deployment.yaml

kubectl apply -f redis/redis-service.yaml

kubectl apply -f user-profile/deployment.yaml

kubectl apply -f user-profile/service.yaml

kubectl apply -f trip-planner/deployment.yaml

kubectl apply -f trip-planner/service.yaml

kubectl apply -f messaging/deployment.yaml

kubectl apply -f frontend/deployment.yaml

kubectl apply -f frontend/service.yaml
```

For specific instructions on how to deploy and test each of the service's components (frontend, messaging, redis, trip-planner, user-profile), please reference the **README.md** files defined in each component's respective directory.