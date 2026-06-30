import os

directories = [
    "src",
    "src/ui",
    "src/controllers",
    "src/services",
    "src/rendering",
    "src/models",
    "src/utils",
    "src/config",
    "assets",
    "tests",
    "docs"
]

for d in directories:
    os.makedirs(d, exist_ok=True)

# Create __init__.py files
for d in directories:
    if d.startswith("src"):
        with open(os.path.join(d, "__init__.py"), "w") as f:
            f.write("")

# Requirements
with open("requirements.txt", "w") as f:
    f.write("PySide6\nmarkdown-it-py\nPygments\nbeautifulsoup4\nJinja2\nwatchdog\npytest\nblack\nruff\nmypy\nrich\nloguru\nmdit-py-plugins\n")

print("Directories and base files created.")
