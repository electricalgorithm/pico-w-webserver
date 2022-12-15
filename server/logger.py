import ulogger
import ntptime
import gc
from machine import RTC

class RealClock(ulogger.BaseClock):
    def __init__ (self):
        self.rtc = RTC()
        ntptime.host = "ntp.ntsc.ac.cn"
        ntptime.settime()

    def __call__(self) -> str:
        y,m,d,_,h,mi,s,_ = self.rtc.datetime()
        return '%d-%d-%d %d:%d:%d' % (y,m,d,h,mi,s)

class uLoggerHandlers:
    FORMAT = "&(time)% - &(level)% - &(msg)%"
    
    def __init__(self, clock_source):
        self.handler_to_term = ulogger.Handler(
            level=ulogger.INFO,
            fmt=uLoggerHandlers.FORMAT,
            clock=clock_source,
            direction=ulogger.TO_TERM,
            colorful=True,
        )

        self.handler_to_file = ulogger.Handler(
            level=ulogger.INFO,
            fmt=uLoggerHandlers.FORMAT,
            clock=clock_source,
            direction=ulogger.TO_FILE,
            file_name="logging.log",
            max_file_size=8*1024
        )
        
    def return_handlers(self):
        return (self.handler_to_term, self.handler_to_file)


class LogUtil:
    def __init__(self):
        self.clock = None
        self.is_connected = False
        
        # Create a temporary logger until connection established.
        temp_handlers = uLoggerHandlers(self.clock)
        self.handlers = temp_handlers.return_handlers()
        self.logger = ulogger.Logger(
            name = __name__,
            handlers = self.handlers
        )
        
    def set_time(self):
        # Call this function after setting a connection to internet.
        self.clock = RealClock()
        self.handlers = uLoggerHandlers(self.clock)
        self.logger = ulogger.Logger(
            name = __name__,
            handlers = self.handlers.return_handlers(),
        )
        
        # Run garbage collector to release old memories.
        gc.collect()

LOG = LogUtil()