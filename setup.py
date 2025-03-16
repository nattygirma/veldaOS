from setuptools import setup, find_packages

setup(
    name="veldaos-core",
    version="0.1.0",
    packages=find_packages(include=["veldaos.core*"]),
    install_requires=[
        "pyautogui>=0.9.54",
        "pillow>=10.0.0",
        "opencv-python>=4.8.0",
        "loguru>=0.7.0",
        "pydantic>=2.0.0",
        "pytesseract>=0.3.10",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.2",
        "numpy>=1.24.0",
    ],
    author="Natnael",
    author_email="nattygirma28@gmail.com",
    description="AI Agent System for OS Automation with OCR and LLM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nattygirma/veldaos",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
) 