# VLC in Docker with Web-based VNC GUI

This project runs VLC media player inside a Docker container with a browser-accessible VNC desktop.

## Steps to Run
1. Build the image:
   ```bash
   docker-compose build
   ```

2. Start the container:
   ```bash
   docker-compose up -d
   ```

3. Access in browser:
   Open [http://localhost:6080](http://localhost:6080)

4. VLC is installed and ready. A sample video is available at `/media/sample.mp4`.

## Credentials
Default VNC password: `123456`

---
**Mentor:** Vimal Daga Sir @ Linux World
