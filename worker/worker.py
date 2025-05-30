import redis

import requests
import json

import psycopg2

def main():
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    postgres_conn = psycopg2.connect(
        dbname='playqueue',
        user='lemonade',
        password='supersecureadminpassword',
        host='postgres',
        port="5432",
    )
    cur = postgres_conn.cursor()
    
    print(r.lrange('task_queue', 0, -1))
    
    try:
        while (True):
            # get task
            print("Waiting for task...")
            next_task = r.blpop('task_queue')
            
            if next_task:
                name, description = next_task
            
            print(f"Got task: {name} with description: {description}. Sending to Ollama...")
            
            # send to ollama
            url = "http://ollama-server:11434/api/generate"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama3.2:latest",
                "prompt": "Make or reference an existing famous line to use as an aesthetic playlist quote around 10 words long, (e.g., 'come sit, breathe my friend, believe you can, and you're halfway there'). Base it on the following description: '" + description + "'. Only output the playlist quote and nothing else.",
                "stream": False
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                # all good!
                response_text = response.text
                data = json.loads(response_text)
                actual_response = data["response"]
            else:
                actual_response = "ERROR: " + response.status_code + ": " + response.text
            
            # push actual_response to postgres
            print(f"Got response: {actual_response}. Pushing into db...")
            
            cur.execute("INSERT INTO results (description) VALUES (%s);", (actual_response,))
            postgres_conn.commit()
            
            # let the frontend know
            requests.post("http://flask-app:5000/notify", json={"status": "success"})
    except KeyboardInterrupt:
        print("Keyboard interrupted. Exiting gracefully...")
        requests.post("http://flask-app:5000/notify", json={"status": "interrupt"})
    
    except psycopg2.Error as e:
        print(f"ERROR: Postgres error: {str(e)}")
        postgres_conn.rollback()
        requests.post("http://flask-app:5000/notify", json={"status": "error", "error": str(e)})
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        requests.post("http://flask-app:5000/notify", json={"status": "error", "error": str(e)})
        
    finally:
        cur.close()
        postgres_conn.close()
            
    
if __name__ == "__main__":
    main()