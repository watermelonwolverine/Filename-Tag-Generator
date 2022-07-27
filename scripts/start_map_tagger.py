import os

from ftg.__cli_wrapper.main import main

main(config=os.path.join("configs", "config.json"),
     tags=os.path.join("configs", "map-tags.json"))
