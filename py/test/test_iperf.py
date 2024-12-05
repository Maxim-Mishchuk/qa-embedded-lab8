import pytest
from parser import parse_iperf_output
from conftest import client, server
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_iperf_output(client):
    logger.info("Testing iperf output...")
    stderr_output = client["stderr"].read().strip()
    if stderr_output:
        logger.error(f"iperf client error: {stderr_output.decode()}")

    assert stderr_output == b'', f"stderr: {stderr_output.decode()}"

    stdout_output = client["stdout"].read()
    logger.info("iperf stdout output received.")
    logger.debug(f"iperf output: {stdout_output.decode()}")

    res = parse_iperf_output(stdout_output.decode())
    logger.info("Parsed iperf output successfully.")

    assert float(res['Transfer']) > 2, f"Transfer too low: {res['Transfer']} {res['Transfer_unit']}"
    assert float(res['Bandwidth']) > 2, f"Bandwidth too low: {res['Bandwidth']} {res['Bandwidth_unit']}"
    logger.info("Test passed successfully.")
