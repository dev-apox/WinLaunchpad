# 🚀 WinLaunchpad

**WinLaunchpad** is an elegant, lightweight, and fluid clone of the famous macOS "Launchpad", natively redesigned for Windows. Developed in Python using Tkinter, it provides a full-screen interface to quickly access all your programs, games, and files while keeping your desktop clean.

## ✨ Key Features

* **⚡ Global Quick Access:** Press `ALT + Q` at any time to instantly show or hide the Launchpad, without interrupting your workflow.
* **🔍 Smart Search:** A responsive search bar allows you to find your applications simply by typing their name.
* **📄 Smooth Pagination:** Navigate through your app pages using the on-screen buttons or your mouse wheel.
* **🎨 Customizable Icons:** Built-in support for `.png`, `.jpg`, or `.icns` icons. If an icon is missing, a minimalist icon with the app's initial is automatically generated.
* **🪟 Immersive Style:** Full-screen design with a semi-transparent dark background for a modern look.

## 🛠️ Prerequisites

To run the source code, ensure you have the following installed:

* [Python 3.8+](https://www.python.org/downloads/)
* The `Pillow` library (for image handling)

You can install the required dependencies with:

```bash
pip install Pillow
```

## 📥 Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/YOUR-USERNAME/WinLaunchpad.git
   cd WinLaunchpad
   ```

2. **The `icone/` Folder (Important!)**
   For your apps to have custom logos, the program uses a folder named `icone`.
   * Create a folder named `icone` in the same directory as the script (it will be created automatically on the first run if missing).
   * Place your icon images in this folder. The filename must match the application's name (all lowercase).
   * *Example:* If the app is named "Google Chrome", you can name the image `google chrome.png`, `google.png`, or `chrome.png`.

3. **Execution**
   Run the main script:

   ```bash
   python launchpad.pyw
   ```

## 💻 Usage

* **Open/Close:** Use the `ALT + Q` keyboard shortcut. Alternatively, press `ESC` or click "Close" in the top right corner to exit.
* **Navigation:** Use the mouse wheel or click the side arrows (`<` and `>`) to scroll through pages.
* **Search:** Simply start typing on your keyboard when the Launchpad is open to filter apps in real-time.

## 👨‍💻 Author

Developed with ❤️ by **DenisDev**.

Feel free to open a *Pull Request* or report *Issues* if you want to contribute to this project!
