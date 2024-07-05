import pika
import time

def receive_msg():
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
    ch.queue_declare(queue='coffee_orders')

    ch2 = conn.channel()
    ch2.queue_declare(queue='tea_orders')

    def callback(ch, method, properties, body):
        print(f' [x] received {body}')
        time.sleep(1)
        print(' [x] done')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch2.basic_qos(prefetch_count=1)
    ch2.basic_consume(queue='tea_orders', on_message_callback=callback)
    
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue='coffee_orders', on_message_callback=callback)
    print(' [*] waiting for msg, to exit press ctrl+c')
    ch.start_consuming()

receive_msg()
