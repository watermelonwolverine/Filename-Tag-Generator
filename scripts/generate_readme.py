from ftg.__help import help_texts

with open("README.md", "wt", encoding="UTF-8") as fh:
    fh.write(help_texts.readme_text)
