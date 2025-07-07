# SCBA Web Scraper

This Python script uses Selenium to scrape data from the [SCBA Sentencias website](https://sentencias.scba.gov.ar/). It allows users to specify a date range, search terms, and select specific "registros" (records like Resolutions or Sentences) and "organismos" (organizations) to search within. The scraped documents are saved as text files in a structured directory.

## Setup

### Prerequisites

*   **Python 3.x:** If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).
*   **Google Chrome:** The script uses ChromeDriver, so you need Google Chrome installed.
*   **ChromeDriver:**
    *   Download the ChromeDriver executable that matches your Google Chrome version from [here](https://chromedriver.chromium.org/downloads).
    *   Place `chromedriver.exe` (or `chromedriver` on Linux/macOS) in the same directory as the `scraper.py` script, or ensure it's in a directory included in your system's PATH environment variable.

### Installation

1.  **Clone the repository (or download the files):**
    ```bash
    # If you have git installed
    # git clone <repository-url>
    # cd <repository-name>

    # Otherwise, just make sure scraper.py is in your working directory
    ```

2.  **Install required Python libraries:**
    Open your terminal or command prompt and run:
    ```bash
    pip install selenium
    ```
    *(If you use a virtual environment, create and activate it before running pip install.)*

## How to Run

1.  **Navigate to the script's directory:**
    Open your terminal or command prompt and change to the directory where `scraper.py` and `chromedriver.exe` are located.

2.  **Run the script:**
    ```bash
    python scraper.py
    ```

3.  **Follow the prompts:**
    The script will ask you to input:
    *   **Fecha desde (DD/MM/AAAA):** Start date for the search.
    *   **Fecha hasta (DD/MM/AAAA):** End date for the search.
    *   **Texto a buscar:** The search term.
    *   **Seleccione 2 o 3 para elegir el registro:**
        *   `2` for "Resoluciones"
        *   `3` for "Sentencias"
        *   `0` to terminate this selection.
    *   **Seleccione un número de organismo:** Choose from the listed organizations. You can select multiple organizations one by one. Enter `0` when you are done selecting organizations.

4.  **Output:**
    The script will create a base folder named `resoluciones` (or `sentencias` depending on your choice). Inside this, it will create subfolders for each selected "organismo". The scraped documents will be saved as `.txt` files within these subfolders.

    Example directory structure:
    ```
    your-project-folder/
    ├── resoluciones/  # This is the base folder created by the script
    │   ├── tipo_de_registro/  # e.g., 'resoluciones' or 'sentencias'
    │   │   ├── NombreDelOrganismo1/
    │   │   │   ├── documento1.txt
    │   │   │   └── documento2.txt
    │   │   └── NombreDelOrganismo2/
    │   │       └── documento3.txt
    ├── scraper.py
    ├── chromedriver.exe  # Or chromedriver (macOS/Linux)
    └── README.md
    ```

## Important Notes

*   **Website Changes:** Web scraping scripts are sensitive to changes in the target website's structure. If the SCBA website is updated, this script might need adjustments.
*   **Scraping Delays:** The script includes random delays (`pausa_aleatoria`) and fixed `time.sleep()` calls to make the scraping process slower and potentially less likely to be blocked by the website. Adjust these timings if necessary, but be respectful of the website's resources.
*   **Error Handling:** The script includes basic error handling for individual document processing and page navigation, allowing it to continue with other tasks if an error occurs. Check the console output for any error messages.
*   **ChromeDriver Path:** The line `s = Service(executable_path='chromedriver.exe')` in `scraper.py` assumes `chromedriver.exe` is in the same directory or in PATH. Modify this path if your ChromeDriver is located elsewhere (e.g., `Service(executable_path='/path/to/your/chromedriver')`).
```
