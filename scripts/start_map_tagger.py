import os
import sys

sys.path.append(os.path.join("..", "src"))

# noinspection PyPep8
from cli_wrapper.main import main

main(os.path.join("tags", "map-tags.json"))
