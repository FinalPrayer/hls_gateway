import os
import signal
import shutil

from . import settings as app_settings
import logging


def stop_inactive_stream():
    from .models import Channel
    for channel in Channel.objects.all():
        if channel.transcode_pid > 0:
            if channel.hitting_count == 0:
                # Running, but no one watching in the past period anymore.
                logging.info("No one watching channel %s, stopping." % channel.nickname)
                process_to_kill = channel.transcode_pid
                try:
                    os.kill(process_to_kill, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                channel.transcode_pid = 0
            else:
                logging.info('%s is still watching' % channel.nickname)
                channel.hitting_count = 0
            channel.save()


def purge_inactive_stream():
    from .models import Channel
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


def deploy_transcode_daemon(channel_object):
    import subprocess
    input_path = channel_object.url
    nickname = channel_object.nickname
    output_path = init_channel_space(nickname)
    f_null = open(os.devnull, 'w')
    execution_process = subprocess.Popen(ffmpeg_command_builder(input_path, nickname, output_path), stdout=f_null)
    logging.info('Channel %s is transcoding under PID %d' % (channel_object.nickname, execution_process.pid))
    return execution_process.pid


def ffmpeg_command_builder(input_url, nickname, output_path):
    from urllib.parse import urlparse
    ffmpeg_command = app_settings.FFMPEG_PATH

    # Base command building phase. This sets the FFMPEG running path, hide all banners, sets only report when error
    # occurred, overrides output file without asking and reduces latency by omitting buffer
    command = [ffmpeg_command, '-hide_banner', '-loglevel', 'error', '-y', '-fflags', 'nobuffer']

    if urlparse(input_url).scheme == 'rtsp':
        # For RTSP, fall back the stream to use TCP instead of UDP for maximum compatibility
        command.extend(['-rtsp_transport', 'tcp'])

    command.extend(['-i', input_url,
                    '-vsync', '0', '-copyts', '-c:v', 'copy', '-c:a', 'copy',
                    '-hls_flags', 'delete_segments+append_list', '-f', 'hls',
                    '-segment_list_flags', nickname + '_live',
                    '-hls_time', '1', '-hls_list_size', '3',
                    '-hls_segment_filename', output_path + '/%d.ts',
                    output_path + '/index.m3u8'])
    return command
