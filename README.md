# Containerized Python Application with Flask and MongoDB on Kubernetes

## Overview

This project demonstrates how to build and deploy a containerized Python application using Flask and MongoDB on a Kubernetes cluster. The application provides a simple REST API for interacting with a bookstore database.

## Project Structure

The project is organized into two main directories:

1.  **api**: This directory contains the source code and configuration files for the Python application and its Docker image.
    *   `app.py`: This file contains the Python code for the Flask application.
    *   `bookstore.json`: This file contains the sample data for the MongoDB database.
    *   `Dockerfile`: This file contains the instructions for building the Docker image for the Flask application.
    *   `requirements.txt`: This file lists the Python dependencies for the Flask application.

2.  **kubernetes**: This directory contains the YAML files for deploying the application and database to a Kubernetes cluster.
    *   `flask-deployment.yaml`: This file defines the Kubernetes deployment for the Flask application.
    *   `mongo-statefulset.yaml`: This file defines the Kubernetes statefulset for the MongoDB database.
    *   `mongo-service.yaml`: This file defines the Kubernetes service for the MongoDB database.
    *   `flask-service.yaml`: This file defines the Kubernetes service for the Flask application.

## Prerequisites

*   A Kubernetes cluster (e.g., Minikube, GKE, AKS)
*   Kubectl command-line tool
*   Docker
*   MongoDB client (optional)

## Installation and Usage

### 1. Set up the Kubernetes Cluster

Start your Kubernetes cluster using Minikube or your preferred provider. Verify the cluster status using:

```bash
kubectl get nodes
```

### 2. Deploy MongoDB

Deploy the MongoDB StatefulSet using the provided YAML file:

```bash
kubectl apply -f kubernetes/mongo-statefulset.yaml
```

This will create a MongoDB instance with one replica. Monitor the pod status until it becomes ready:

```bash
kubectl get pods
```

### 3. Expose MongoDB

Expose the MongoDB instance outside the cluster using a service:

```bash
kubectl apply -f kubernetes/mongo-service.yaml
```

This will create a LoadBalancer service that can be accessed from outside the cluster.

### 4. Import Data into MongoDB

Get the MongoDB URI using:

```bash
export MONGO_URI=mongodb://$(minikube service mongodb --url | sed 's,.*/,,')
```

Import the sample data into MongoDB:

```bash
mongoimport --file=api/bookstore.json --collection=bookstorecollection --uri=$MONGO_URI --jsonArray --db=bookstoredatabase
```

### 5. Build and Push the Docker Image

Build the Docker image for the Flask application:

```bash
docker build -t <your-dockerhub-username>/<docker-image>/
```

Push the image to your Docker Hub repository:

```bash
docker push <your-dockerhub-username>/<docker-image>
```

### 6. Deploy the Flask Application

Deploy the Flask application using the provided YAML file:

```bash
kubectl apply -f kubernetes/flask-deployment.yaml
```

This will create a deployment with one replica. The image will be pulled from your Docker Hub repository.

### 7. Expose the Flask Application

Expose the Flask application outside the cluster using a service:

```bash
kubectl apply -f kubernetes/flask-service.yaml
```

This will create a LoadBalancer service that can be accessed from outside the cluster.

### 8. Test the Application

Access the Flask application using the service's external IP or `minikube service flask` command.

## Documentation

The project includes detailed explanations and instructions in the following files:

*   `README.md`: This file provides a comprehensive guide to installing and using the system.
*   `api/Dockerfile`: This file explains how the Docker image for the Flask application is built.
*   `kubernetes/*.yaml`: These files explain the Kubernetes resources used to deploy the application and database.

## Submission

Students must submit the following:

*   Entire source code for the Python program (`api` directory)
*   YAML files for Kubernetes resources (`kubernetes` directory)
*   Documentation with explanations and detailed instructions (`README.md`)

This project provides a hands-on experience in building and deploying a containerized Python application on Kubernetes. By following the instructions and completing the submission requirements, students will gain valuable skills in containerization, orchestration, and cloud-native development.