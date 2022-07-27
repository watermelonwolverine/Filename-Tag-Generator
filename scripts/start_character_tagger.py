import os

from ftg.__cli_wrapper import main

main.main(config=os.path.join("configs", "config.json"),
          tags=os.path.join("configs", "character-tags.json"))
