from ftg.__help import help_text

with open("README.md", "wt", encoding="UTF-8") as fh:
    fh.write(help_text.readme_text)
