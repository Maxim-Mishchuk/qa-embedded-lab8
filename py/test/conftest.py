import paramiko
import pytest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SSHData:
    def __init__(self, ip, username, port, keyPath):
        self.ip = ip
        self.username = username
        self.port = port
        self.keyPath = keyPath

sshServer = SSHData('127.0.0.1', 'vagrant', 2222, "F:/КПІ/4/QA/lab8/.vagrant/machines/master/virtualbox/private_key")
sshClient = SSHData('127.0.0.1', 'vagrant', 2200, "F:/КПІ/4/QA/lab8/.vagrant/machines/slave/virtualbox/private_key")

@pytest.fixture(scope="function")
def server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    logger.info("Connecting to the server via SSH...")
    ssh.connect(
        hostname=sshServer.ip,
        username=sshServer.username,
        port=sshServer.port,
        key_filename=sshServer.keyPath
    )
    logger.info("Starting iperf server...")
    ssh.exec_command('iperf -s &')
    logger.info("iperf server started.")

    yield ssh

    logger.info("Stopping iperf server...")
    ssh.exec_command('pkill iperf')
    ssh.close()
    logger.info("Server connection closed.")

vm_server_ip = '10.0.0.1'

@pytest.fixture(scope="function")
def client(server):
    connect = "iperf -c {server_ip} -p 5001"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    logger.info("Connecting to the client via SSH...")
    ssh.connect(
        hostname=sshClient.ip,
        username=sshClient.username,
        port=sshClient.port,
        key_filename=sshClient.keyPath
    )
    logger.info("Starting iperf client...")
    stdin, stdout, stderr = ssh.exec_command(connect.format(server_ip=vm_server_ip))
    logger.info("iperf client command executed.")

    yield {
        "ssh": ssh,
        "stdin": stdin,
        "stdout": stdout,
        "stderr": stderr,
    }

    logger.info("Stopping iperf client...")
    ssh.exec_command('pkill iperf')
    ssh.close()
    logger.info("Client connection closed.")
