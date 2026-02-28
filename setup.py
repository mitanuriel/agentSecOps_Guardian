from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentSecOps_Guardian",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python-based security operations agent project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/agentSecOps_Guardian",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "fastapi>=0.111.0",
        "uvicorn>=0.30.0",
    ],
)
