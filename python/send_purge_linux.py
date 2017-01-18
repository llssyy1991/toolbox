import pika

server_ip = "10.0.126.20"
command = "purge-linux"
global response
response = None


def handle_purge_linux_response(ch, method, props, body):
    global response
    response = body
    ch.basic_ack(delivery_tag = method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(server_ip))

channel = connection.channel()

channel.queue_declare( queue = "purge-linux")
channel.queue_declare( queue = "purge-linux-response")
channel.basic_consume(handle_purge_linux_response, queue='purge-linux-response')

channel.basic_publish(
    exchange='',
    routing_key='purge-linux',
    properties=pika.BasicProperties(
        reply_to='purge-linux-response',
    ),
    body=str(command)
)

while response == None:
    connection.process_data_events()
print response

