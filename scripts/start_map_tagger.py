import os

from cli_wrapper.main import main


main(os.path.join("configs", "config.json"),
     os.path.join("configs", "map-tags.json"))
