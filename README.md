# Fibonacci Service

This project is a production-ready, containerized web service that computes 
Fibonacci numbers based on user input. The application is designed to be scalable,
testable, observable, and cloud-agnostic. It includes built-in Prometheus metrics,
CI/CD integrations, Docker support, and Helm charts for Kubernetes deployments.

---

## Features

- RESTful API implemented in Python using the `http.server` standard library
- Returns the first `n` Fibonacci numbers via a query parameter (`n`)
- Prometheus metrics exposed at `/metrics` for observability
- Built-in validation and error handling for edge cases
- Dockerized and ready for deployment to multiple cloud platforms
- Helm chart for Kubernetes-based deployment
- CI/CD support via GitHub Actions, GitLab CI, Jenkins, and CircleCI

---

## Running the Application Locally

1. Clone the repository.
2. Navigate to the `python/` directory.
3. Install dependencies:

    ```bash
    python3 -m pip install -r requirements.txt
    ```

4. Start the application:

    ```bash
    python3 main.py
    ```

The application will start on [http://localhost:8000](http://localhost:8000), and Prometheus metrics will be available at [http://localhost:8001/metrics](http://localhost:8001/metrics).

Test the service using:

```bash
curl "http://localhost:8000/?n=5"
```

Expected response:

```
0, 1, 1, 2, 3
```

---

## Running Tests

1. Ensure `pytest` is installed:

    ```bash
    python3 -m pip install --user pytest
    ```

2. Run the test suite:

    ```bash
    python3 -m pytest test_main.py
    ```

The test suite includes:

- Validation of correct Fibonacci output
- Proper exception handling for edge cases and limits
- Prometheus metrics validation

---

## Docker Support

To build and run the application in a Docker container:

```bash
docker build -t ewaa113/fibonacci:latest ./python
docker run -d --name fibonacci -p 8000:8000 -p 8001:8001 ewaa113/fibonacci:latest
```

---

## Kubernetes Deployment (Helm)

Install using Helm:

```bash
helm install fibonacci ./charts/fibonacci
```

To customize values:

```bash
helm install fibonacci ./charts/fibonacci --set image.repository=ewaa113/fibonacci,image.tag=latest
```

---

## CI/CD Integration

- **GitHub Actions** – Triggered on push or PR to `main`
- **GitLab CI** – Build, test, docker-build, and deploy stages
- **Jenkins** – Declarative multi-stage pipeline
- **CircleCI** – Unit testing support

---

## Cloud Deployment Support

The application supports deployment to:

- Heroku
- Azure Web App
- AWS Elastic Beanstalk
- Google Cloud Run

Secrets for each cloud must be configured in your CI/CD tool or deployment environment.

---

## Environment & Dependencies

- Python 3.9+
- `prometheus_client`
- `pytest`

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

---

For any questions related to this submission, please feel free to reach out.
