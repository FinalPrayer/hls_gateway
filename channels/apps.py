import time
from multiprocessing import Process

from django import db
from django.apps import AppConfig
from django.conf import settings

from channels import helper


class AutoStopService(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        while True:
            time.sleep(10)
            helper.stop_inactive_stream()
            helper.purge_inactive_stream()


class ChannelsConfig(AppConfig):
    name = 'channels'

    def ready(self):
        auto_stop = AutoStopService()
        auto_stop.start()
