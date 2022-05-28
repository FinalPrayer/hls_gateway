from django.conf import settings


def get(key, default):
    return getattr(settings, key, default)


# Settings for Channels
HLS_HEARTBEAT_CHECK_SECONDS = get('HLS_HEARTBEAT_CHECK_SECONDS', 10)
HLS_STREAM_ROOT = get('HLS_STREAM_ROOT', settings.BASE_DIR / 'channel_static')
FFMPEG_PATH = get('FFMPEG_PATH', 'ffmpeg')
