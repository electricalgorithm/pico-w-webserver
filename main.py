import machine
from picozero import pico_temp_sensor
from server.logger import LOG
from server.server import PicoServer
from server.device import Device

WIFI_SSID = '[SSID_HERE]'
WIFI_PASSWORD = '[PASS_HERE]'

def main():
    board = Device()
    server = PicoServer(WIFI_SSID, WIFI_PASSWORD)
    if server.connect(max_try=50):
        server.update_time_from_online()
        server.start(80)
        server.serve(board)
    
        server.stop()

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        Device.reset_board()

    except Exception as error:
        LOG.logger.error("Exception: ", error)
        Device.reset_board()
