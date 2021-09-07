import os
import subprocess
import time

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .forms import ChannelAddForm
from .models import Channel
from helper import init_channel_space


# Create your views here.
def channel_add(request):
    form = ChannelAddForm()
    if request.method == 'POST':
        form = ChannelAddForm(request.POST)
        if form.is_valid():
            channel = Channel()
            channel.nickname = form.cleaned_data['nickname']
            channel.url = form.cleaned_data['url']
            channel.save()
            return redirect(reverse(channel_list))
    context = {
        'form': form
    }
    return render(request, 'channel_add.html', context)


def channel_del(request, channel):
    if request.method == 'POST':
        channel = Channel.objects.get(nickname=request.POST['channel'])
        channel.delete()
        return redirect(reverse(channel_list))
    else:
        context = {
            'channel': Channel.objects.get(nickname=channel)
        }
        return render(request, 'channel_delete.html', context)


def channel_list(request):
    context = {
        'channels': Channel.objects.all()
    }
    return render(request, 'channel_list.html', context)


def channel_open(request, nickname):
    channel = Channel.objects.get(nickname=nickname)
    if channel is None:
        raise Http404("Channel does not exist")
    # Status that channel is not yet started:
    if channel.transcode_pid < 1:
        input_path = channel.url
        ffmpeg_command = os.getenv('FFMPEG_PATH', default='ffmpeg')
        output_path = init_channel_space(nickname)
        f_null = open(os.devnull, 'w')
        command_parameters = [ffmpeg_command, '-hide_banner', '-loglevel', 'error',
                              '-y', '-fflags', 'nobuffer', '-rtsp_transport', 'tcp', '-i', input_path,
                              '-vsync', '0', '-copyts', '-c:v', 'copy', '-c:a', 'copy', '-hls_flags',
                              'delete_segments+append_list', '-f', 'hls', '-segment_list_flags', nickname + '_live',
                              '-hls_time', '1', '-hls_list_size', '3', '-hls_segment_filename', output_path + '/%d.ts',
                              output_path + '/index.m3u8']
        execution_process = subprocess.Popen(command_parameters, stdout=f_null)
        channel.transcode_pid = execution_process.pid
        channel.hitting_count = 1
        channel.save()
        index_path = os.path.join(settings.BASE_DIR, 'channel_static', nickname, 'index.m3u8')
        for i in range(0, 10):
            if not os.path.exists(index_path):
                time.sleep(1)
    return redirect(reverse(channel_read, args=[nickname, 'index.m3u8']))


def channel_read(request, channel, filename):
    try:
        file_stream = open(os.path.join(settings.BASE_DIR, 'channel_static', channel, filename), 'rb')
        extension = filename.split('.')[1]
        if extension == 'm3u8':
            response = HttpResponse(file_stream, content_type='application/vnd.apple.mpegurl')
        elif extension == 'ts':
            response = HttpResponse(file_stream, content_type='video/MP2T')
        else:
            response = HttpResponse(file_stream)
        channel_data = Channel.objects.get(nickname=channel)
        channel_data.hitting_count = channel_data.hitting_count + 1
        channel_data.save()
        return response
    except FileNotFoundError:
        raise Http404("file does not exist")
