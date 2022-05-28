FROM python:3.9.12
ARG TARGETARCH
ARG TARGETPLATFORM
ENV HLS_STREAM_ROOT=/output

USER root

WORKDIR /tmp
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-${TARGETARCH}-static.tar.xz
RUN tar -xf ffmpeg-release-${TARGETARCH}-static.tar.xz
RUN FOLDER=$(tar tf ffmpeg-release-${TARGETARCH}-static.tar.xz | head -1 | cut -f1 -d"/") && mv $FOLDER/ffmpeg /bin && rm -r $FOLDER
RUN chmod +x /bin/ffmpeg
RUN rm ffmpeg-release-${TARGETARCH}-static.tar.xz
RUN mkdir -p /output

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
