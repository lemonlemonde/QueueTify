hewwo :3

# What am I looking at?
This is a learning project for backend stuff. (Tech stack below).

Premise is something like: 

1. user queues job through dashboard (generate playlist name based on input description)
2. task put in Redis queue
3. containerized worker picks up job
4. does the job (Ask ollama server (llama3.2) to generate playlist name)
5. writes to PostgreSQL db
6. displayed in dashboard!
wow!


## Quick Start with just Docker Compose
1. `docker compose up`
2. `docker exec -it ollama-server ollama pull llama3.2:latest`
    - or do this from Docker desktop
    - only need to do this once!
    - unless you delete the image :3
3. go to browser `localhost:5000`


# I need more details
no
(jk)

## Tech stack:
- Gunicorn
- Eventlet
- PostgreSQL
- Redis
- Docker
- Flask
    - Flask-WTF
    - Flask-SocketIO

## To be incorporated later:
- Ansible
- Make
- Kubernetes
- nginx


## Architecture:
![image_overarching](./images/IMG_5318.jpg)
![image_websocket](./images/IMG_5321.jpg)