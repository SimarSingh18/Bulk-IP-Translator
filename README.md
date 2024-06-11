# IP to DNS Converter

A simple desktop application that converts IP addresses to domain names using Python and the Tkinter GUI toolkit. The application allows users to select a CSV file containing IP addresses, processes the IP addresses to resolve their domain names, and saves the results to a new CSV file.

## Features

- Supports CSV files with:
  - One column with no header.
  - One column with a header.
  - Multiple columns with a "DESTIP" column.
- Concurrent processing of IP addresses to improve performance.
- Simple and user-friendly interface.
- Allows users to select the input CSV file and save the output CSV file to a desired location.

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Install Required Packages

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ip-to-dns-converter.git
   cd ip-to-dns-converter
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

- `tkinter` for the graphical user interface.
- `PIL` (Pillow) for image processing.
- `pandas` for data manipulation.
- `concurrent.futures` for concurrent processing.

## Usage

1. Run the application:

   ```bash
   python app.py
   ```

2. The main window will appear with a "Browse CSV File" button. Click the button to select your input CSV file.

3. The application will process the IP addresses in the selected CSV file, resolving them to domain names.

4. You will be prompted to choose a directory to save the output CSV file. The output file will be saved with a timestamped filename.

## Project Structure

```
ip-to-dns-converter/
├── app.py                # Main application file
├── process.py            # Processing logic for IP to domain name conversion
├── requirements.txt      # List of required Python packages
└── README.md             # This README file
```

## Code Explanation

### Main Application (`app.py`)

- **App Class**: Initializes the main window, sets up the UI elements, and handles user interactions.
- **setup_ui()**: Sets up the user interface components.
- **setup_buttons()**: Creates and places the buttons.
- **setup_labels()**: Creates and places the labels.
- **setup_logo()**: Loads and places the logo image.
- **browse_file()**: Handles file selection and initiates the processing.
- **prompt_save_dialog()**: Prompts the user to select a save location for the output file.
- **revert_button_color()**: Resets the button color after the click action.

### Processing Logic (`process.py`)

- **process_ip(ip)**: Resolves a single IP address to a domain name.
- **process_csv(input_file)**: Processes the input CSV file, resolves IP addresses to domain names concurrently, and saves the results to a new CSV file.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
