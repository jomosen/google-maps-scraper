import logging

logging.basicConfig(
    level=logging.DEBUG,  # puedes subirlo a INFO si no quieres tanto detalle
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("app")
