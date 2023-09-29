import logging
import subprocess

from es.home import App

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    logger.info("Starting streamlit server")
    subprocess.Popen(["streamlit", "run", "src/es/modules/analytics.py", "--server.headless", "true"])
    
    logger.info("Starting application")
    app = App()
    app.run()
