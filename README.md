# Python_Arena

## Description
In this I am going to start some python projects with the goal of working on some smaller AI works.

# Python Projects

## AI_InEasySteps Folder
This is a folder captures the work created from the book **Artificial Intelligence for Developers (in easysteps)*** by Richard Urwin. Check out the ReadMe file with-in that folder
for explaination on the various works completed.

# Python_Playground Folder
This folder covers projects from the **Python Playground (Second Edition)** by Mahesh Venkitachalam. The ReadMe file with-in this folder will explain the projects available.

## pdf_keyword_search.py
Ability to provide a list of words to be identified within a folder holding PDF files. It will search each PDF for the word or words and create a CSV file with the results of the word used and which PDF file (by name) has it.
This one was personally created and not from any book or publication.

`py pdf_keyword_search.py`

## mazeGenerator.py
Draw a maze using a grid layout. This gave me the idea to create a maze game for my website at dochano.com.

`py mazeGenerator.py`


# Preparing
The following steps will allow for you to pull down the projects and get them to work locally. I elected to place this after the projects so you can determine if there is interest before installing.

## Install Python
[Python Install](https://www.python.org/downloads)

Be sure to check the **Add python.exe to the PATH** box. Then choose **Custom Installation.** Then **Next**. And another **Next** to **Finish**.

## Installing PIP
<!-- CTRL+E to get the special single quote -->
`python -m ensurepip --upgrade`
or
`python.exe -m pip install --upgrade pip`

## Installing pygame
Pygame allows for graphics to be created.
`pip install pygame`

## To Install Tensorflow you need 3.11.9 version
Python 3.13 will not work with Tensorflow at this time.

### Set up Virtual Environment
I ran into issue with switching between 3.11 and 3.13 due to permissioning issues with running the python scripts.

So I went with creating a virtual environment for 3.11 using the following:
`py -3.11 -m venv venv311`

When I want to run a script inside that environment I just need to enter in the following:
`venv311\Scripts\activate`

Then I can run the script like normal. Note that the virtual environment is a path to a activate bash script so take note of the virtual environments full path for future reference.

## Install Tensor Flow
Need Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017, 2019, and 2022.
https://learn.microsof.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170

Be sure to run this in the virtual environment.

`pip install tensorflow`

`pip install tensorflow_datasets`

`pip install matplotlib`

# Other Installs
To allow for speeding up the neural networks training process the following is suggested. I found it was not required.

## Install WSL2
https://learn.microsoft.com/en-us/windows/wsl/install

> [!IMPORTANT]
> **To launch Ubuntu enter `wsl.exe -d Ubuntu`.**

Regular Update and upgrade packages required. So make the following a habit:
`sudo apt update && sudo apt upgrade`
https://learn.microsoft.com/en-us/windows/wsl/setup/environment

Using **Windows Terminal** you can enter `Ctrl+Shift+P` to get the **Command Palette**.
https://learn.microsoft.com/en-us/windows/terminal/install#invoke-the-command-palette

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

**Linux and Bash**
https://learn.microsoft.com/en-us/windows/wsl/tutorials/linux

> [!CAUTION]
> Tensor Flow requires Python 3.8, 3.9, 3.10, 3.11. Which means Python 3.12+ is not yet supported. Version of Python as of this writing is 3.13.3.
> Using WSL2 you can install Python 3.11 and pip (using `pyenv`).

## Install pyenv with Python version 3.11.9
1. From CMD prompt enter in `wsl.exe -d Ubuntu`.
2. Enter `sudo apt update`.
3. Enter ```sudo apt install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl \
    llvm libncursesw5-dev xz-utils tk-dev libxml2-dev \
    libxmlsec1-dev libffi-dev liblzma-dev git```
4. Enter `curl https://pyenv.run | bash`
5. Then Enter in the following:
   ```
   # Add pyenv to shell
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init -)"' >> ~/.bashrc
   exec "$SHELL"
   ```
6. Enter `pyenv install 3.11.9`.
7. Enter `pyenv global 3.11.9`.


## Install CuDNN and CUDA toolkit
https://docs.nvidia.com/deeplearning/cudnn/installation/linux.html

> [!WARNING]
> If above doesn't work then you should follow steps [Install pyenv with Python version 3.11.9](#Install-pyenv-with-Python-version-3.11.9).
> Used **ChatGPT** to assist in resolution.
