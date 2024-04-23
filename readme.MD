# Desktop App Project

## Overview

This desktop application is built with Flet and designed to perform scraping tasks on provided input data. It scrapes data from specific URLs, processes it, and generates an output file. The application utilizes various libraries such as Pandas, Requests, Jinja2, and Cloudscraper for data manipulation, web scraping, and rendering.

## Features

- Supports input data in CSV and Excel formats.
- Scrapes data from Reuter and Sanitino websites.
- Provides progress updates during scraping.
- Generates an output Excel file with formatted data.
- Allows cancellation of the scraping process.

## Requirements

- Python 3.x
- Flet
- Pandas
- Requests
- Jinja2
- Cloudscraper

## Installation

1. Clone the repository:

   ```shell
   git clone <repository-url>
   ```

2. Create and activate virtual environment:

   ```shell
   python3 -m venv venv && source venv/bin/activate
   ```

3. Install dependencies:

   ```shell
   pip3 install -r requirements.txt
   ```

## Usage

1. Run the `main.py` file:

   ```python
   flet run main.py
   ```

2. Select the input file using the provided file picker.
3. Click "Start Collecting Data" to initiate the scraping process.
4. Monitor the progress and view messages in the application interface.
5. Once scraping is complete, find the output Excel file in the same directory as the input file.

## Build app

To build and publish your app for different OS [check this link](https://flet.dev/docs/publish).

## Contribution

Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to customize the README according to your project's specific details and requirements!