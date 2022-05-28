import os
import time

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from . import settings as app_settings
from .forms import ChannelAddForm
from .models import Channel
from channels import helper


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
        helper.deploy_transcode_daemon(channel)
        for i in range(0, 10):
            if not helper.channel_ready(nickname):
                time.sleep(1)
    return redirect(reverse(channel_read, args=[nickname, 'index.m3u8']))


def channel_read(request, channel, filename):
    try:
        file_stream = open(os.path.join(app_settings.HLS_STREAM_ROOT, channel, filename), 'rb')
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
