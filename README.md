hewwo :3

## What am I looking at?
This is a learning project for backend stuff. (Tech stack below).

Premise is something like: 

- user queues job through dashboard (generate playlist name)
- task put in Redis
- containerized worker picks up job
- does the job
- writes to PostgreSQL db
- displayed in dashboard!
wow!


## I need more details
Too bad!
(jk)

Devlog and stuff are in your Obsidian repo, duh. It's called `orange` if you don't remember

## Tech stack:
- PostgreSQL
- Ansible
- Redis
- Docker
- Kubernetes
- nginx
- Flask
- Make


## Quick start:
1. Installations
- docker
- ollama

```shell
ollama pull llama3.2:latest
```

2. Start up everything
You'll need different windows cause the processes are all running
```shell
ollama serve
docker compose up

uv init
uv venv
uv sync

conda deactivate # if (base) is haunting you
source .venv/bin/activate

python worker/worker.py
```

> [!note] 
> `docker compose up -d` if you don't wanna see the funky logs
> and idk how to run Ollama server as detached daemon in macOS....


3. Submit a job!
```shell
# Example
python jobs/submit_job.py 
```