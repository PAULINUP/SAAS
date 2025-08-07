# setup.py
from setuptools import setup, find_packages

setup(
    name="qcore-system",
    version="1.0.0",
    description="Q-Core AI System - Plataforma de IA explicável com predição, simulação e análise simbiótica.",
    author="Paulo Geovane da Silva Souza",
    author_email="paulobravo_23@hotmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "fpdf",
        "qiskit",
        "pdfminer.six",
        "spacy",
        "streamlit"
    ],
    entry_points={
        "console_scripts": [
            "qcore-run=api_gateway:app"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
