# README.md

# CosmicChronicle

CosmicChronicle is a Python project that automates the fetching of NASA's Astronomy Picture of the Day (APOD) and commits it to a GitHub repository. The project runs twice a day using GitHub Actions.

## Project Structure

```
CosmicChronicle
├── etl_apod.py          # Main script for fetching and processing APOD
├── apod                 # Directory for storing downloaded images and Markdown files
├── requirements.txt     # Python dependencies
├── .gitignore           # Files and directories to ignore in Git
├── .gitattributes       # Git LFS tracking for images
└── .github/workflows/apod_etl.yml  # GitHub Actions workflow for automation
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CosmicChronicle
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your NASA API key as a GitHub Actions secret named `NASA_API_KEY`.

## Usage

The project is designed to run automatically via GitHub Actions. Once set up, it will fetch the Astronomy Picture of the Day and store it in the `apod` directory.

## License

This project is licensed under the MIT License.