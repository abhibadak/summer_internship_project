import streamlit as st
import psutil
import os
import shutil
import docker
from datetime import datetime

st.set_page_config(page_title="Automation Panel", layout="wide")
st.title("🔧 Automation Panel Dashboard")

# 1️⃣ System Status Monitor
st.header("🖥️ System Monitor")
col1, col2 = st.columns(2)
with col1:
    st.metric("CPU Usage", f"{psutil.cpu_percent()}%")
with col2:
    memory = psutil.virtual_memory()
    st.metric("RAM Usage", f"{memory.percent}%")

# 2️⃣ Folder Backup
st.header("🗂️ Folder Backup")
backup_path = st.text_input("Enter folder path to backup:")
backup_dir = "backups"
os.makedirs(backup_dir, exist_ok=True)

if st.button("Create Backup"):
    if os.path.exists(backup_path):
        folder_name = os.path.basename(backup_path.rstrip("/\\"))
        time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination = os.path.join(backup_dir, f"{folder_name}_{time_stamp}")
        shutil.copytree(backup_path, destination)
        st.success(f"Backup created at {destination}")
    else:
        st.error("Invalid folder path!")

# 3️⃣ Docker Container Control
st.header("🐳 Docker Control Panel")
try:
    client = docker.from_env()
    containers = client.containers.list(all=True)

    for container in containers:
        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            st.write(f"{container.name} ({container.status})")
        with col2:
            if st.button(f"Start {container.name}", key=container.name + "_start"):
                container.start()
                st.success(f"Started {container.name}")
        with col3:
            if st.button(f"Stop {container.name}", key=container.name + "_stop"):
                container.stop()
                st.warning(f"Stopped {container.name}")
except Exception as e:
    st.error(f"Error accessing Docker: {e}")

# 4️⃣ Shell Command Execution
st.header("🖱️ Run Shell Command")
command = st.text_input("Enter shell command")

if st.button("Execute"):
    try:
        output = os.popen(command).read()
        st.code(output)
    except Exception as e:
        st.error(f"Error: {e}")
