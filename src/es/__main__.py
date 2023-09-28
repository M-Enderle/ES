from es.home import Tk, mainFrame
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting application")
    root = Tk()
    root.tk.call('tk', 'scaling', 1.7)
    app = mainFrame(root)
    root.mainloop()