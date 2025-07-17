import gradio as gr
import psutil
import os
import shutil
from datetime import datetime
import docker

# Docker Client
try:
    client = docker.from_env()
except Exception as e:
    client = None
    docker_error = str(e)

# 🖥️ System Monitor
def system_status():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    return f"CPU Usage: {cpu}%\nRAM Usage: {ram}%"

# 📂 Folder Backup
def backup_folder(path):
    if not os.path.exists(path):
        return f"❌ Path not found: {path}"
    folder_name = os.path.basename(path.rstrip("/\\"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join("backups", f"{folder_name}_{timestamp}")
    os.makedirs("backups", exist_ok=True)
    try:
        shutil.copytree(path, dest)
        return f"✅ Backup created at: {dest}"
    except Exception as e:
        return f"❌ Error: {e}"

# 🐳 Docker Container Management
def docker_status():
    if not client:
        return f"Docker not connected: {docker_error}"
    try:
        containers = client.containers.list(all=True)
        result = ""
        for c in containers:
            result += f"{c.name} ({c.status})\n"
        return result or "No containers found"
    except Exception as e:
        return f"❌ Error: {e}"

def start_container(name):
    try:
        container = client.containers.get(name)
        container.start()
        return f"✅ Started container: {name}"
    except Exception as e:
        return f"❌ Error: {e}"

def stop_container(name):
    try:
        container = client.containers.get(name)
        container.stop()
        return f"✅ Stopped container: {name}"
    except Exception as e:
        return f"❌ Error: {e}"

# 💻 Shell Executor
def run_command(cmd):
    try:
        output = os.popen(cmd).read()
        return output or "(No output)"
    except Exception as e:
        return f"❌ Error: {e}"

# 🖥️ Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🛠️ Automation Panel using Gradio")

    with gr.Tab("System Monitor"):
        status_btn = gr.Button("Get System Status")
        status_output = gr.Textbox(label="Status")
        status_btn.click(system_status, outputs=status_output)

    with gr.Tab("Folder Backup"):
        folder_input = gr.Textbox(label="Folder Path")
        backup_btn = gr.Button("Create Backup")
        backup_output = gr.Textbox(label="Backup Status")
        backup_btn.click(backup_folder, inputs=folder_input, outputs=backup_output)

    with gr.Tab("Docker Control"):
        docker_btn = gr.Button("List Containers")
        docker_output = gr.Textbox(label="Containers")
        docker_btn.click(docker_status, outputs=docker_output)

        container_input = gr.Textbox(label="Container Name")
        start_btn = gr.Button("Start")
        stop_btn = gr.Button("Stop")
        docker_action_output = gr.Textbox(label="Action Output")
        start_btn.click(start_container, inputs=container_input, outputs=docker_action_output)
        stop_btn.click(stop_container, inputs=container_input, outputs=docker_action_output)

    with gr.Tab("Shell Command"):
        cmd_input = gr.Textbox(label="Enter Command")
        run_btn = gr.Button("Run")
        cmd_output = gr.Textbox(label="Command Output")
        run_btn.click(run_command, inputs=cmd_input, outputs=cmd_output)

demo.launch()