import os
import signal
import shutil

from django.conf import settings


def stop_inactive_stream():
    from .models import Channel
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
    from .models import Channel
    for channel in Channel.objects.all():
        if channel.transcode_pid == 0:
            channel_path = os.path.join(settings.BASE_DIR, 'channel_static', channel.nickname)
            if os.path.exists(channel_path):
                shutil.rmtree(channel_path)


def init_channel_space(stream_nickname):
    output_path = os.path.join(settings.BASE_DIR, 'channel_static', stream_nickname)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for file in os.listdir(output_path):
        os.remove(os.path.join(output_path, file))
    return output_path
