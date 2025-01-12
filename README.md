# Product URL Crawler

This project is a web crawler that scans specified domains and extracts product URLs based on predefined patterns. The extracted URLs are saved to an `output.json` file.

## Setup and Installation

Follow the steps below to set up the environment, install the dependencies, and run the crawler.

### 1. Create a Virtual Environment

First, navigate to your project directory and create a virtual environment. You can do this by running the following command:

```bash
python -m venv venv
```
This will create a venv folder in your project directory that contains a new isolated environment.

### 2. Activate the Virtual Environment

For Windows:

```bash
.\venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all the necessary libraries specified in the requirements.txt file.

### 4. Run the Crawler

To run the crawler and extract product URLs, execute the following command:

```bash
python scraper.py
```

This will start the crawling process for the domains specified in the script.

### 5. Check the Output

After the crawler finishes, you will find the product URLs in the `output.json` file located in your project directory.
