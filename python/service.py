import pika

class service():

    # change these things for latter use
    ip_address = "10.0.126.20"
    linux_purge_queue = "purge-linux"
    windows_purge_queue = "purge-windows"
    linux_purge_response = "purge-linux-response"
    windows_purge_response = "purge-windows-response"
    power_off_queue = "power-off"
    power_off_response = "power-off-response"
    application_start_queue = "application-start"
    linux_start = "linux-start"

    def __init__(self, service_queue, service_callback):

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.ip_address, heartbeat_interval = 0))
        self.channel = self.connection.channel()
        for queue in service_queue:
            self.channel.queue_declare( queue = queue )
            self.channel.basic_consume(service_callback, queue = queue)

    def service_start(self):
        self.channel.start_consuming()

class service_caller():

    ip_address = "10.0.126.20"
    linux_purge_queue = "purge-linux"
    windows_purge_queue = "purge-windows"
    linux_purge_response = "purge-linux-response"
    windows_purge_response = "purge-windows-response"
    power_off_queue = "power-off"
    power_off_response = "power-off-response"
    application_start_queue = "application-start"
    linux_start = "linux-start"

    def __init__(self, mode, service_queue, command, response_queue = None):
        self.response = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.ip_address, heartbeat_interval = 0))
        self.channel = self.connection.channel()
        self.channel.queue_declare( queue = service_queue )
        if response_queue != None:
            self.channel.queue_declare( queue = response_queue)
        print "connection created"
        self.channel.basic_publish(
            exchange='',
            routing_key=service_queue,
            properties=pika.BasicProperties(
                reply_to=response_queue,
            ),
            body=str(command)
        )
        if mode == "no_response":
            while self.response == None:
                self.connection.process_data_events()
            print self.response


    def responses(self, ch, method, props, body):
        self.response = body
        ch.basic_ack(delivery_tag = method.delivery_tag)