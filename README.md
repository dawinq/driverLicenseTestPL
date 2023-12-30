# Polish Driver License Question Visualization Program

## Overview

This program is designed to visualize Polish driver's license questions.

### How to Use

#### For Windows

- **Option 1: Use Pre-built Executable**
  1. Download `main.exe` from the `dist` folder.

  2. Download visual data: [Visual Data (ZIP)](https://www.gov.pl/pliki/mi/wizualizacje_do_pytan_27.06.2023.zip)
  
  3. Extract all visual data to `data/visuals/` folder (in parts due to many files).

  4. Download question data: [Question Data](https://www.gov.pl/attachment/1e683ccd-6293-4656-9c16-fab2628b0c46)
  
  5. Place the Excel file inside `data/questions/`

  6. Run the executable on your Windows system.

  7. Load question data.

  8. Load visual data.
 

- **Option 2: Build Executable Yourself**
  1. Download the repository.
  2. Create a Python virtual environment:
     ```bash
     pip install virtualenv
     python3 -m venv venv
     .\venv\Scripts\activate
     ```
  3. Download required Python modules:
     ```bash
     pip install -r requirements.txt
     ```
  4. Build the executable:
     ```bash
     pyinstaller --onefile main.py
     ```

  5. Download visual data: [Visual Data (ZIP)](https://www.gov.pl/pliki/mi/wizualizacje_do_pytan_27.06.2023.zip)

  6.  Extract all visual data to `data/visuals/` folder (in parts due to many files).

  7. Download question data: [Question Data](https://www.gov.pl/attachment/1e683ccd-6293-4656-9c16-fab2628b0c46)

  8.  Place the Excel file inside `data/questions/`

  9. Run the program.

  10. Load question data.

  11. Load visual data.

#### For Linux

  1.  Run `main.py` after installing required Python modules:
  ```bash
  pip install -r requirements.txt
  ```

  2. Download visual data: [Visual Data (ZIP)](https://www.gov.pl/pliki/mi/wizualizacje_do_pytan_27.06.2023.zip)
  
  3.  Extract all visual data to `data/visuals/` folder (in parts due to many files).

  4. Download question data: [Question Data](https://www.gov.pl/attachment/1e683ccd-6293-4656-9c16-fab2628b0c46)

  5.  Place the Excel file inside `data/questions/`

  6. Run the program.

  7. Load question data.

  8. Load visual data.

### Additional information

For more details on the Polish driver's license, visit the [official website](https://www.gov.pl/web/infrastruktura/prawo-jazdy).

## License 

This program is open-source and licensed under [MIT License](https://chat.openai.com/c/LICENSE).


Feel free to adjust or customize it further to match your preferences!
