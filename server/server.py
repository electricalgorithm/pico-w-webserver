import network
import socket
from time import sleep
from server.logger import LOG
from server.views import home_page

class PicoServer:
    def __init__(self, ssid, password):
        self.WIFI_SSID = ssid
        self.WIFI_PASSWORD = password
        # Internal attributes
        self.wlan = self._setup_network()
        self.ip_addr = None
        self.socket = None
        
    def _setup_network(self):
        # Set-up the WiFi driver on station mode.
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        LOG.logger.info("Stationary mode activated.")
        return wlan
        
    def connect(self, max_try=25):
        self.wlan.connect(self.WIFI_SSID, self.WIFI_PASSWORD)
        LOG.logger.info("Trying to connect to AP: ", self.WIFI_SSID)
        # Wait for a handshake.
        try_count = 0
        LOG.logger.info("Waiting for handshake.")
        while not self.wlan.isconnected():
            print(".", end="")
            try_count += 1
            sleep(0.5)
            
            if try_count >= max_try:
                print()
                LOG.logger.error("Couldn't established a handshake to AP.")
                return False
        
        print()
        LOG.logger.info("Connection established. The board is online.")
        # Save the IP address.
        self.ip_addr = self.wlan.ifconfig()[0]
        LOG.logger.info("Local IP of the board is ", self.ip_addr)
        return True
    
    def start(self, port):
        address = (self.ip_addr, port)
        self.socket = socket.socket()
        LOG.logger.info("Socket has created.")
        
        # Try to bind the address.
        self.socket.bind(address)
    
        # Listen for client connections.
        self.socket.listen(1)
        LOG.logger.info("Socket is started to listen on %s:%d." % address)
        LOG.logger.info(self.socket)
    
    def stop(self):
        self.socket.close()
        
    def serve(self, device_instance):
        while True:
            LOG.logger.info("Accepting connections.")
            client = self.socket.accept()[0]
            request = str(client.recv(1024))
            LOG.logger.info("Request catched.")
            
            # Split the request header into method and query.
            request = request.split()
            request_method = request[0]
            request_query = request[1]
            LOG.logger.info("HTTP Recieved: [%s] %s" % (request_method, request_query))
            
            # Update states.
            device_instance.update_information()
                
            if request_query == "/":
                pass
            elif request_query == "/enable":
                LOG.logger.info("LED enable is catched.")
                device_instance.led_set_high()
            elif request_query == "/disable":
                LOG.logger.info("LED disable is catched.")
                device_instance.led_set_low()

            web_page = home_page(
                device_instance.states["TEMP"],
                device_instance.states["LED"],
                device_instance.states["CLOCK"]
            )
            client.send(web_page)
            client.close()

    def update_time_from_online(self):
        # Update RTC timer, and therefore logger.
        if self.wlan.isconnected():
            try:
                LOG.set_time()
                LOG.logger.info("Time has been updated from online.")
            except OSError as error:
                LOG.logger.error("Time couldn't be updated due to error: ", error)
        else:
            LOG.logger.error("Time couldn't be set because WLAN connection is not established.")
