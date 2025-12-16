from setuptools import setup, find_packages

setup(
    name="horloq",
    version="0.1.0",
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
