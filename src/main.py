from flask import Flask

from services.nuclei.nuclei import NucleiScanner
from shared.utils.initialize_icon import initialize_icon
from shared.utils.log_handler import LogHandler

logger = LogHandler(logger_name=__name__)
app = Flask(__name__)

initialize_icon()
print("teste")
logger.info("TESTE DE INFO")
logger.error("TESTE DE ERROR")
logger.warn("Teste DE WARNING")


@app.route("/")
def hello_world():
    return {"service": "Kaio-Ken Defender API", "version": "0.1.0", "status": "running"}


nuclei = NucleiScanner(timeout=10000).exec(target="https://google.com")
