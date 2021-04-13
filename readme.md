# HLS Gateway
HLS Gateway is a Python Django based web app that serves theoretically
any live-streaming sources into HLS (HTTP Live Streaming), and serves
them over HTTP protocol, for players (or web browsers) supporting it.

## Introduction
HLS Gateway is built with the need of changing protocol from RTSP
stream into HLS, as some online streaming services, or surveillance
cameras, does not provide HLS streams, which can be played using
ExoPlayer within Android Systems, or web browsers.

Another package, [rtsp-stream](https://github.com/Roverr/rtsp-stream),
provides an out-of-the-box RTSP to HLS converter, same as this
project. However, such package cannot detect inactivity of any stream
within a short period, which causes huge traffic if the package is
used as a stream gateway, and the user switches between multiple
streams in such a period. In addition, this package cannot transcode
audio stream even if the audio is enabled in setting.

## Technology Explained
FFMpeg is required as a dependency for this software. User firstly
sets the input link and the nickname into the database. After the
setup, user can watch the HLS stream using provided address.

If FFMpeg is downloaded/compiled without adding into `PATH`, you can
specify the path of FFMpeg by setting the environmental parameter
`FFMPEG_PATH` to the corresponding executable location.

## Installation
As this project is still under early development, deployment onto
production is not yet supported. User can still install the software
for testing.

### Requirement
This project is written Using Django 3.0, which requires Python 3.6
and above, with PIP module installed.

I am strongly recommended installing and running this software using
a virtual environment.

Firstly, ensure you have Python 3.6 and above, with virtual
environment and PIP installed. You can find it under terminal or
command-line using:

```
python --version
python -m pip --version
python -m venv
```

You should expect the version number of both Python and PIP, with the
usage of `venv` printed onto the screen.

If you are running on certain OSs, that both Python 2 and Python 3 is
installed, you may get Python 2.x returned using above command. If
so, try the following command:

```
python3 --version
python3 -m pip --version
python3 -m venv
```

### Installing Procedure
The procedure is written for installation using virtual environment.
To get started, firstly clone the project down to your computer.
Then, create a virtual environment by typing:

```
python -m venv virtualenv
```

or

```
python3 -m venv virtualenv
```

if your system still having python 2 installed.

This will create a folder called `virtualenv` under the current
working directory. You can rename `virtualenv` to anything you want.

Then, get into the virtual environment folder just created, and run
the command based on your operating system and environment:

```
# UNIX based system (Linux, BSD, MacOS) with bash, zsh or sh.
source bin/activate
# for users using csh
source bin/activate.csh
# For Windows users using command-line
bin\activate.bat
# For Windows users using PowerShell
bin\activate.ps
```

Once the virtual environment is activated, go back to this project's
root folder and run the following command to install all
requirements:

```
pip install -r requirements.txt
```

## Usage
To start the server, firstly activate the virtual environment created
for this project (if you have followed the installation step above),
then run the following command. Note this software is still under
early development, and it is not recommended using it on production
environment yet.

```
python manage.py runserver --noreload
```

This will start a server with address http://127.0.0.1:8000/

the following path is available on the software:

- `/hls_gateway/admin/list/` - The main entry of this software,
  lists all transcoding addresses and nickname associated. You can
  add your own channel by pressing the "Add a Channel" link.
- `/hls_gateway/watch/{nickname}` - entry to watch the stream, where
  the `nickname` is the nickname you set on adding the stream.
- `/hls_gateway/read/{nickname}/{filename}` is the link used to read
  the HLS stream. You are not required to use this link, as the entry
  link above will automatically forward to this link.
  
The procedure of using this software is:

- Add your own RTSP source onto the system, with a nickname of your
  choice
- Once added, open `/hls_gateway/watch/{nickname}` with players
  supporting HLS, where `nickname` is what you have set on last step.

## Development Roadmap
This project is still under early development, and more features are
developing, including the composing of this readme document.

The following known bug fixes will be addressed in later development:

- If this software is running in a server with low-end performance,
  it may fail to return the playlist data when the channel is called
  before transcoding started.
- Default page when accessing the frontpage is not yet implemented.
  
The following Features will also be implemented:

- Docker Support
- Multiple live input format will also be included
- authentication
- Batch import

Under the roadmap, the following features are in lower priority, but
it may be implemented if time allowed.

- Playlist generation with TVG metadata 
- Multiple user support
