import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/p5-linux-server-config/")

# Entry point for this application.
# Import the main app code

from catalog_main import app as application
