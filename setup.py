from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dengyan-poker",
    version="1.0.0",
    author="liyk1997",
    author_email="",
    description="干瞪眼扑克游戏Python实现",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liyk1997/DengYanPoker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Board Games",
    ],
    python_requires=">=3.7",
    install_requires=[
        # 当前版本只使用标准库，无需额外依赖
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "dengyan-poker=main:main",
        ],
    },
)