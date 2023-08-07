# ESTHER-Ontology

ESTHER is the ontology for rhetorical figures in English: esther.owl contains the formal domain ontology, describing rhetorical figures 
in the English language. It is also accessible via <a href="ramonakuehn.de/esther.owl">ramonakuehn.de/esther.owl </a>

The 10 competency questions written in SPARQL in Python are in the file CompetencyQuestions.py
The tool that supports people in the annotation process is in the folder FyF. The installation guide is below.


## Installation

1. Download and install Python from https://www.python.org/downloads/
2. Within this project's directory, create a Virtual Environment to separate this project from other projects on your computer.
   ```powershell
   # current directory is ESTHER-Ontology
   python -m venv ./venv
   ```
3. Activate your new Virtual Environment (depending on your OS, you need to execute a different script). If the activation was successful you will se a `(venv)` in front of your terminal line
   ```powershell
   # for windows Powershell
   ./venv/Scripts/Activate.ps1
   ```
4. Install all dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run the script from within the `FyF` folder
   ```powershell
   cd ./FyF
   python Find_Your_Figure.py
   ```
