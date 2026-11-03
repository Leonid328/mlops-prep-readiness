# Pre-course readiness (Leonid328)

Three checks: Docker, Compose + Redis, k3s. No ML.

## Task 1

```bash
python3 -m venv venv && . venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --port 8000
# other terminal:
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/echo -H 'Content-Type: application/json' -d '{"message":"hi"}'
docker build -t prep-task1 .
docker run --rm -d -p 8000:8000 --name prep-task1 prep-task1
docker stop prep-task1
```

## Task 2

Redis is `redis://redis:6379`, not localhost. Named volume `redis-data`.

```bash
docker compose up --build -d
curl -s -X POST http://127.0.0.1:8000/increment/test
# three times -> 1, 2, 3
```

Vagrantfile boots Ubuntu, installs Docker, forwards 8000. On a VPS without nested virt (`/dev/kvm` missing) run the same `scripts/provision.sh` on the Ubuntu host instead of `vagrant up`. Compose networking is unchanged.

Why Vagrant vs compose on a laptop: same Ubuntu + Docker for everyone on the course, not "works on my Mac only". Compose still runs inside that VM.

## Task 3

k3s, 3 replicas, `INSTANCE_ID` = pod name, Service NodePort 30080.

```bash
k3s kubectl apply -f k8s/
k3s kubectl get pods
curl -s http://127.0.0.1:30080/health
k3s kubectl scale deploy/prep-task1 --replicas=1
k3s kubectl scale deploy/prep-task1 --replicas=3
k3s kubectl delete pod -l app=prep-task1 --field-selector=status.phase=Running | head
```
