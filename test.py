import pika
import uuid
import json
import time

class CodeRunner:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='direct_exchange', exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, code, problem):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='direct_exchange',
            routing_key='run_code',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps({'code': code, 'problem': problem})
        )
        return self.wait_for_result()

    def wait_for_result(self, timeout=30, interval=0.5):
        start_time = time.time()
        while self.response is None:
            self.connection.process_data_events()
            if time.time() - start_time > timeout:
                return {"error": "Timeout waiting for response"}
            time.sleep(interval)
        return self.response

def main():
    code_runner = CodeRunner()
    
    # Test messages
    test_cases = [
        {
            'code': 'print("Hello, World!")',
            'problem': {
                'test_cases': [{'input': [], 'expected_output': 'Hello, World!'}]
            }
        },
        {
            'code': 'def add(a, b): return a + b\nprint(add(2, 3))',
            'problem': {
                'test_cases': [{'input': [2, 3], 'expected_output': 5}]
            }
        }
    ]
    
    for case in test_cases:
        print(f"Sending request: {case['code']}")
        response = code_runner.call(case['code'], case['problem'])
        print(f"Received response: {response}")
        print("---")

if __name__ == "__main__":
    main()