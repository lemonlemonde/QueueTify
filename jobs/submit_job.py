import redis
import argparse

def main(args):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    print(f"Adding task for description: {args.description}")
    r.rpush('task_queue', args.description)
    
    print(r.lrange('task_queue', 0, -1))
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('description', type=str, help='Description of the playlist name. Surround with quotations("hi hi") for whitespace.')
    
    args = parser.parse_args()
    main(args)