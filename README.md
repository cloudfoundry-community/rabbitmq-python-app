# rabbitmq-python-app
This simple CF python app uses the pika(http://pika.readthedocs.io/en/0.10.0/index.html) library to send and receive message to a rabbitmq service on Cloud Foundry.

## Requirments
- Need to have rabbitmq service on CF space
- Update manifest.yml to have the right rabbitmq service NAME

## Usage
```
cf push
```
Visit the URL and if it says "OK" then your rabbitmq is good!
