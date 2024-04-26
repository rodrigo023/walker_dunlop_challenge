# walker_dunlop_challenge
Challenge for Walker &amp; Dunlop interview process

# Content
- [walker\_dunlop\_challenge](#walker_dunlop_challenge)
- [Content](#content)
- [Architecture](#architecture)
- [Assumptions](#assumptions)
- [Limitations](#limitations)
- [Areas for improvement](#areas-for-improvement)
- [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Install dependencies](#install-dependencies)
    - [Start the service](#start-the-service)
- [Unit tests](#unit-tests)
    - [Install Pytest](#install-pytest)
    - [Run the unit tests](#run-the-unit-tests)
- [API docs](#api-docs)

# Architecture
![Architecture Diagram](architecture.png)
The architecture relies on the fan-out pattern. This allows publishing a message to an SNS Topic with multiple SQS Subscriptions.
Each SQS Subscription has it's own Subscription filter policy so it only consumes the messages concerning to that particular SQS Queue. This mechanism makes possible to, by just publishing a single message to the SNS Topic, have multiple Queues consuming those messages and only processing those that are of interest to each of those Queues.\
An example of a Subscription filter policy would be:
 ```json
{
  "email": [
    {
      "exists": true
    }
  ]
}
```
The above filter will take only the messages that are supposed to be sent by Email to the Users.

# Assumptions
- An external Database or API provides the User data, like Email or Phone. For the sake of simplicity, a User table was created to provide this data.
- The external source of User's data provides a unique id to identify each user. In this service a user_id is used to match the User's data with the User's preferences.
- The implementation of the code that sends the Email or SMS notifications is out of scope.

# Limitations

# Areas for improvement
- Exception handling
- Define a logging strategy and an appropriate logging library
- Implement authentication and authorization for the API endpoints. Potentially use RBAC to control which clients can access the /preferences/ endpoints and the /notifications/ endpoint.
- Run performance tests to validate the /notifications/ endpoint behavior. What happens when sending a notification to thousands of users? Or even millions of users?

# Setup
### Prerequisites
- A PostgreSQL instance running on an accessible location

### Install dependencies
```console
$ pip install -r requirements.txt
```

### Start the service
```console
$ uvicorn src.main:app
```
This will start the service on http://127.0.0.1:8000

# Unit tests
### Install Pytest
```console
$ pip install pytest
```

### Run the unit tests
```console
$ pytest
```

# API docs
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
