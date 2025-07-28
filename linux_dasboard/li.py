import streamlit as st
import paramiko

st.set_page_config(page_title="Linux SSH Terminal", page_icon="🖥", layout="centered")

st.title("🖥 Linux SSH Terminal Web App")
st.markdown("Execute Linux commands on your remote server securely from the browser.")

with st.sidebar:
    st.header("🔐 SSH Credentials")
    hostname = st.text_input("Host", value="your-server-ip")
    port = st.number_input("Port", value=22)
    username = st.text_input("Username", value="ec2-user")
    password = st.text_input("Password", type="password")

st.divider()

command = st.text_input("💻 Enter Command", placeholder="e.g., ls -l /home")

if st.button("Run Command"):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=int(port), username=username, password=password)

        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            st.code(output, language="bash")
        if error:
            st.error(error)
        ssh.close()

    except Exception as e:
        st.error(f"❌ SSH Connection Failed: {e}")