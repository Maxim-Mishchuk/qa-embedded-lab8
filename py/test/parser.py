import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_iperf_output(output):
    logger.info("Parsing iperf output...")
    result = {}

    transfer_match = re.search(r'\s+(\d+\.\d+)\s+(GBytes|MBytes)\s+(\d+\.\d+)\s+(Gbits/sec|Mbits/sec)', output)
    if transfer_match:
        result['Transfer'] = float(transfer_match.group(1))
        result['Transfer_unit'] = transfer_match.group(2)
        result['Bandwidth'] = float(transfer_match.group(3))
        result['Bandwidth_unit'] = transfer_match.group(4)
        logger.info(f"Parsed data: {result}")
    else:
        logger.warning("No matching data found in iperf output.")

    return result
