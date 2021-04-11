import time
from multiprocessing import Process
import os
import signal

from django import db
from django.apps import AppConfig
from django.conf import settings


class AutoStopService(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        from .models import Channel
        while True:
            time.sleep(10)
            for channel in Channel.objects.all():
                if channel.transcode_pid > 0:
                    if channel.hitting_count == 0:
                        # Running, but no one watching in the past period anymore.
                        print("No one watching channel %s, stopping." % channel.nickname)
                        process_to_kill = channel.transcode_pid
                        try:
                            os.kill(process_to_kill, signal.SIGTERM)
                        except ProcessLookupError:
                            pass
                        channel.transcode_pid = 0
                    else:
                        print('%s is still watching' % channel.nickname)
                        channel.hitting_count = 0
                    channel.save()


class ChannelsConfig(AppConfig):
    name = 'channels'

    def ready(self):
        auto_stop = AutoStopService()
        auto_stop.start()
