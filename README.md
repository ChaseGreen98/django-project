Setup (Python 3.12 Virtual Environment)

This project requires Python 3.12. To run it in an isolated environment:

1. Install Python 3.12

Download from python.org
.

Make sure to check “Add Python to PATH” during installation.

2. Create & Activate Virtual Environment
# Create the virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Or activate (Command Prompt)
.\venv\Scripts\activate.bat

3. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install pcpartpicker

4. Run the Project

5. Deactivate When Done
deactivate


Always activate the venv before running the project to ensure the correct Python version and dependencies are used.