import pika

def send_msg(exchange_type='fanout', exchange_name='test_exchange', routing_key=''):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
    
    ch.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
    
    msgs = [
        'msg 1: cofee order',
        'msg 2: tea order',
        'msg 3: juice order',
        'msg 4: smoothie order',
    ]

    for msg in msgs:
        ch.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=msg
        )
        print(f"sent '{msg}' with routing key: '{routing_key}'")

    conn.close()

# send_msg(exchange_type='fanout', exchange_name='fanout_exchange')

# send_msg(exchange_type='direct', exchange_name='direct_exchange', routing_key='order.coffee')
# send_msg(exchange_type='direct', exchange_name='direct_exchange', routing_key='order.tea')

# send_msg(exchange_type='topic', exchange_name='topic_exchange', routing_key='order.hot.coffe')
send_msg(exchange_type='topic', exchange_name='topic_exchange', routing_key='order.*')

