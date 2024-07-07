import pika
import time
import json
import docker
import tempfile
import os
import shutil

def create_runnable_scripts(code, problem):
    # Placeholder for creating runnable scripts
    exec_script = "print('Execution script')"
    solution_script = f"print('Solution script')\n{code}"
    return exec_script, solution_script

def temp_docker_mounting_folder(exec_script, solution_script, test_cases):
    temp_dir = tempfile.mkdtemp()
    with open(os.path.join(temp_dir, "execution_script.py"), "w") as dest:
        dest.write(exec_script)
    with open(os.path.join(temp_dir, "solution.py"), "w") as dest:
        dest.write(solution_script)
    with open(os.path.join(temp_dir, "test_cases.json"), "w") as dest:
        dest.write(json.dumps(test_cases))
    os.mkdir(os.path.join(temp_dir, "results"))
    return temp_dir

def run_in_docker(code, problem):
    exec_script, solution_script = create_runnable_scripts(code, problem)
    temp_dir = temp_docker_mounting_folder(exec_script, solution_script, problem['test_cases'])

    client = docker.from_env()
    try:
        container = client.containers.run(
            "python:3.9-slim",
            command=["python", "/app/execution_script.py"],
            volumes={temp_dir: {"bind": "/app", "mode": "ro"},
                     os.path.join(temp_dir, "results"): {"bind": "/results", "mode": "rw"}},
            detach=True,
            mem_limit="250m",
            cpu_quota=50000,
            network_mode="none",
            read_only=True,
            user="nobody",
        )
        container.wait(timeout=30)
        
        output_file_path = os.path.join(temp_dir, "results", "results.json")
        with open(output_file_path, "r") as file:
            output = json.loads(file.read())
        
        return {"outputs": output, "error": None}
    except Exception as e:
        return {"outputs": {}, "error": str(e)}
    finally:
        shutil.rmtree(temp_dir)

def receive_msg(exch_type, exch_name, binding_key):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
    ch.exchange_declare(exchange=exch_name, exchange_type=exch_type)
    resp = ch.queue_declare(queue='', exclusive=True)
    queue_name = resp.method.queue
    ch.queue_bind(exchange=exch_name, queue=queue_name, routing_key=binding_key)

    def process_req_clb(ch, method, properties, body):
        req_body = json.loads(body.decode())
        print('Processing request:', req_body)
        
        # Run code in Docker
        result = run_in_docker(req_body['code'], req_body['problem'])
        
        # Send result back to sender
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=json.dumps(result)
        )
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue=queue_name, on_message_callback=process_req_clb)
    print('Worker is waiting for messages. To exit press CTRL+C')
    ch.start_consuming()

receive_msg(exch_type='direct', exch_name='direct_exchange', binding_key='run_code')