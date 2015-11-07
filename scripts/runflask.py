from timesyncsolver import app
import os
import logging

log = logging.getLogger(__name__)

app.run(host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("DEBUG", False))
