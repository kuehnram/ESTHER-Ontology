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

## Acknowledgement
The project on which this report is based was funded by the German Federal Ministry of Education and Research (BMBF) under the funding code 01IS20049. The authors are responsible for the content of this publication.

<img src="https://github.com/user-attachments/assets/5e1ca975-704b-417b-958a-9fbfb6a893d8" width="400" height="300">

