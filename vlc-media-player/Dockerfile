FROM dorowu/ubuntu-desktop-lxde-vnc

# Install VLC
USER root
RUN apt-get update && apt-get install -y vlc curl &&     apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a media directory and add a test video
RUN mkdir -p /media &&     curl -o /media/sample.mp4 https://filesamples.com/samples/video/mp4/sample_640x360.mp4

# Expose port for web VNC
EXPOSE 80

# Default command
CMD ["bash", "-c", "vlc & supervisord -n"]
