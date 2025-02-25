# sdev140
to use this program you need to clone this repository and set up a virtual environment.
here are some instructions:
To set up a virtual environment for Python in Visual Studio Code (VS Code), follow these steps:

Open your project folder in VS Code.

Press Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (macOS) to open the Command Palette.

Type "Python: Create Environment" and select it from the list14.

Choose "Venv" as the environment type4.

Select the Python interpreter you want to use as the base for your virtual environment4.

VS Code will create the virtual environment, typically in a folder named ".venv" in your project directory4.

Once created, VS Code will prompt you to select the new environment as your workspace interpreter. Click "Yes" to use it5.

VS Code will automatically activate the virtual environment when you open a new terminal3.

If you have a requirements.txt file in your project, VS Code will offer to install the packages listed in it4.

After setting up the virtual environment, you can install additional packages using pip in the VS Code terminal:

bash
pip install package_name
To ensure you're using the correct environment, check the bottom-left corner of VS Code for the Python interpreter path, which should point to your virtual environment35.

Remember to add the virtual environment folder (e.g., .venv) to your .gitignore file if you're using version control4.
