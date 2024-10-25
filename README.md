# chatbot_sample

## 1. build docker image

```
docker buld -t chatbot-sample ./
```
## 2. run container
```
docker run -d -p 8507:8507 --name chatbot-sample chatbot-sample
```