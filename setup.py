from setuptools import setup, find_packages
from pathlib import Path

# horloq/__init__.py からバージョンを読み込む
init_file = Path(__file__).parent / "horloq" / "__init__.py"
version = None
with open(init_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

if not version:
    raise RuntimeError("バージョン情報が見つかりません")

setup(
    name="horloq",
    version=version,
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0",
        "Pillow>=10.0.0",
        "pytz>=2023.3",
        "PyYAML>=6.0",
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "horloq=horloq.__main__:main",
        ],
    },
    python_requires=">=3.11",
)
