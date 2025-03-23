import logging
from app import app

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        logger.info("Starting the application...")
        # Try alternative port if 5000 is busy
        try:
            app.run(host='0.0.0.0', port=5000, debug=True)
        except OSError:
            logger.info("Port 5000 is busy, trying port 5001...")
            app.run(host='0.0.0.0', port=5001, debug=True)
    except Exception as e:
        logger.error(f"Failed to start the application: {str(e)}")
        raise
