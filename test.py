import pika
import time

def receive_msg(exchange_type='fanout', exchange_name='test_exchange', binding_key=''):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()

    ch.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    result = ch.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    ch.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

    print(f'waiting for {exchange_name}, binding key: {binding_key}')

    def clb(ch, method, properties, body):
        print(f'received {body.decode()}')
        time.sleep(1)
        print('---done---')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue=queue_name, on_message_callback=clb)
    ch.start_consuming()

# receive_msg(exchange_type='fanout', exchange_name='fanout_exchange')
# receive_msg(exchange_type='direct', exchange_name='direct_exchange', binding_key='order.coffee')
# receive_msg(exchange_type='direct', exchange_name='direct_exchange', binding_key='order.tea')

receive_msg(exchange_type='topic', exchange_name='topic_exchange', binding_key='order.hot.coffe')