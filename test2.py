import pika

def send_messages():
    # Establish a connection to RabbitMQ
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # Create the first channel
    ch1 = conn.channel()
    ch1.queue_declare(queue='coffee_orders')
    ch1.basic_publish(exchange='', routing_key='coffee_orders', body='coffe1')
    ch1.basic_publish(exchange='', routing_key='coffee_orders', body='coffe2')

    # Create the second channel
    ch2 = conn.channel()
    ch2.queue_declare(queue='tea_orders')
    ch2.basic_publish(exchange='', routing_key='tea_orders', body='tea1')
    ch2.basic_publish(exchange='', routing_key='tea_orders', body='tea2')

    print(' [x] messages sent')
    
    # Close the connection
    conn.close()

send_messages()
