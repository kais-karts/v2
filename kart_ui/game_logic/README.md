# Kart UI
## Description
This is code that runs on the **Raspberry Pi**. It serves as the UI _and_ game logic.

_This sub-system shouldn't be run on its own (it's pretty much the top-level integration thing), instead run `main.py` in the parent directory_.



## Installation
There's a bug in the [p5](https://github.com/p5py/p5/tree/master) library, so follow these installation steps:
1. Create a new Python 3.10 environment in Visual Studio Code (`Ctrl+Shift+P` > `Python: Create Environment...`)
    1. Make sure this also installs `requirements.txt`. If not, do `pip install -r requirements.txt`
2. Install `p5` using `pip install p5 --no-dependencies`