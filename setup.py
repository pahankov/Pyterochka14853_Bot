from setuptools import setup, find_packages

setup(
    name="pyterochka_bot",
    version="0.1",
    packages=find_packages(include=["*"]),
    install_requires=[
        "aiogram==3.2.0",
        "aiohttp==3.9.0",
        "python-dotenv==1.0.0",
        "requests==2.32.3",
        "colorlog==6.8.2",
        "Pillow==10.3.0",
        "imageio==2.34.0",  # Добавлено
        "numpy==1.26.4"     # Добавлено
    ],
    extras_require={
        "dev": [
            "pytest==8.3.4",
            "pytest-asyncio==0.25.3",
            "pytest-mock==3.14.0"
        ]
    }
)
