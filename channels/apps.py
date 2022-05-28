import time
from multiprocessing import Process

from django.apps import AppConfig

from . import helper
from . import settings as app_settings


class AutoStopService(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        while True:
            time.sleep(app_settings.HLS_HEARTBEAT_CHECK_SECONDS)
            helper.stop_inactive_stream()
            helper.purge_inactive_stream()


class ChannelsConfig(AppConfig):
    name = 'channels'

    def ready(self):
        auto_stop = AutoStopService()
        auto_stop.start()
