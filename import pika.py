import pika
import time

def receive_messages(exchange_type='fanout', exchange_name='test_exchange', binding_key=''):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = conn.channel()

    # Declare the exchange
    channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    # Declare a queue with a random name
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the exchange
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

    print(f' [*] Waiting for messages from exchange: {exchange_name}, binding key: {binding_key}. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(1)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()

# Example usage:
# Uncomment and modify these lines to experiment with different combinations

# Fanout Exchange (binding key is ignored)
# receive_messages(exchange_type='fanout', exchange_name='fanout_exchange')

# Direct Exchange
receive_messages(exchange_type='direct', exchange_name='direct_exchange', binding_key='order.coffee')
receive_messages(exchange_type='direct', exchange_name='direct_exchange', binding_key='order.tea')

# Topic Exchange
# receive_messages(exchange_type='topic', exchange_name='topic_exchange', binding_key='order.#')  # Matches any order
# receive_messages(exchange_type='topic', exchange_name='topic_exchange', binding_key='order.hot.*')  # Matches hot drinks
# receive_messages(exchange_type='topic', exchange_name='topic_exchange', binding_key='order.*.coffee')  # Matches any coffee order

# To run different scenarios, uncomment the desired function calls and adjust parameters as needed.