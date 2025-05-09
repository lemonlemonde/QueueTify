import redis
import argparse

def submitJob(description):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    print(f"Adding task for description: {description}")
    r.rpush('task_queue', description)
    
    print(r.lrange('task_queue', 0, -1))

def main(args):
    submitJob(args.description)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('description', type=str, help='Description of the playlist name. Surround with quotations("hi hi") for whitespace.')
    
    args = parser.parse_args()
    main(args)