from setuptools import setup, find_packages

setup(
    name="crewbot",
    version="0.1.0",
    description="轻量级多Agent协作平台",
    author="CrewBot Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "pydantic==2.6.0",
        "httpx==0.26.0",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "crewbot=crewbot.__main__:main",
        ],
    },
)