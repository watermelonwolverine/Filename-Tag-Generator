import os

from ftg.__cli_wrapper.main import run_with


run_with(os.path.join("configs", "config.json"),
         os.path.join("configs", "map-tags.json"))
