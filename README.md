# 🐹 HamsterX

Welcome to the **HamsterX** repository! 🚀 This script automates different tasks such as managing hamster skin achievements, card achievements, and generating referral links. Built with asynchronous Python for high efficiency and performance.

## ✨ Features

- ⚡ Support Multi Account
- 🎨 **Hamster Skin** automation.
- 🔗 **Referral Link** generation.
- 🕵️‍♂️ Support for **proxy** usage.
- 📂 Uses external data and proxy files for flexible input management.

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mmdyb/HamsterX.git
   ```
2. Navigate to the project folder:
   ```bash
   cd HamsterX
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## JavaScript Code to Get Data in Telegram Desktop App

Paste this into console and add result to **data.txt**
```
copy(localStorage.getItem('authToken'))
```

## 🚀 Usage

```
python main.py
```

You can run the script using different action options:

- `1`: Automates **Hamster Skin**.
- `2`: Generates **Referral Links**.

### Basic Example:

```bash
python main.py --data data.txt --proxy proxy.txt --action 1
```

### Available Commands:

- `--data` or `-D`: Provide the path to your data file (default: `data.txt`).
- `--proxy` or `-P`: Provide the path to your proxies file (default: `proxies.txt`).
- `--action` or `-A`: Select the action to perform. Choose between `1`, `2`, `3`.

### 📄 Data File Format

Make sure that your `data.txt` file contains your account information, each on a new line, with at least 10 characters per line.

### 🌐 Proxy File Format

Your `proxies.txt` file should contain proxies, one per line, with a valid proxy format.

## 📝 Example Menu

If no action is provided, the script will display a menu to select an option interactively:

```
1. Hamster Skin
2. Generate Referral Links
0. Exit
```

## 📁 Output

- Referral links are saved in `referral.txt` after generation.
  
## 🛠️ Built With

- **Python** 🐍
- **aiofiles** for asynchronous file handling.
- **argparse** for command-line argument parsing.
- **asyncio** for asynchronous task management.

## 📢 Contributing

Feel free to fork this project and submit pull requests. Contributions, issues, and feature requests are welcome!

## ⚠️ Disclaimer

This script is for educational purposes only. Use it responsibly.

## 🎉 Credits

- Developed by: [Mmd](https://github.com/CallMyNameStar)
- Version: 1.0
