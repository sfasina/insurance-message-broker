Insurance Claims Prototype

About the project
This project simulates an event-driven architecture of an insurance company. It handles the asynchronous reception and processing of insurance claims.

How it works
The system consists of three main, independent components running in Docker containers:

Claim Gateway (FastAPI) - The entry API gateway. It receives HTTP requests from clients and instantly forwards the messages.
Apache Kafka - A distributed message broker (KRaft mode) that securely stores messages in a queue.
Fraud Detector (Python) - A background worker script. It continuously reads messages from Kafka and performs validation checks.

Features

Receives JSON data regarding insurance claims via a REST API.
Responds to the client immediately (200 OK) without waiting for actual data processing.
Asynchronously evaluates messages in the background and flags potential fraud (e.g., claimed amount over 50,000).
Automated build and execution of the entire environment using Docker Compose.
Automated integration checks via GitHub Actions (CI pipeline).

How to run the project

Ensure you have Docker installed and running.

In the project root directory, execute the command:
docker compose up --build -d

Open the Swagger UI to test and submit data:
http://localhost:8000/docs

To monitor the background data processing, view the detector's logs:
docker compose logs -f fraud-detector
