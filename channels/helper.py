import os
import signal
import shutil

from django.conf import settings
from . import settings as app_settings
from .models import Channel


def stop_inactive_stream():
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


def purge_inactive_stream():
    for channel in Channel.objects.all():
        if channel.transcode_pid == 0:
            channel_path = os.path.join(app_settings.HLS_STREAM_ROOT, channel.nickname)
            if os.path.exists(channel_path):
                try:
                    shutil.rmtree(channel_path)
                except FileNotFoundError:
                    pass


def init_channel_space(stream_nickname):
    output_path = os.path.join(app_settings.HLS_STREAM_ROOT, stream_nickname)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for file in os.listdir(output_path):
        os.remove(os.path.join(output_path, file))
    return output_path


def channel_ready(stream_nickname):
    """
    Detect whether the channel is ready to feed.
    """
    stream_path = os.path.join(app_settings.HLS_STREAM_ROOT, stream_nickname)
    fragment_count = 0
    for file in os.listdir(stream_path):
        if file.split('.')[-1] == "ts":
            fragment_count += 1
    return fragment_count > 2
