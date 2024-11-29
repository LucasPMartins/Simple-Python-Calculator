<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=1e81b0&height=120&section=header"/>

[![Typing SVG](https://readme-typing-svg.herokuapp.com/?font=JetBrains+Mono&color=1e81b0&size=45&center=true&vCenter=true&width=1000&lines=Simple+Python+Calculator)](https://git.io/typing-svg)

## ❔ About

This repository contains a Simple Python-based calculator application built using the PySide6 library for the graphical user interface. The application features a grid of buttons for input, a display for showing the current input and results, and an info label for additional information.

### Features

- **Basic Arithmetic Operations**: Supports addition, subtraction, multiplication, division, and exponentiation.
- **Error Handling**: Displays error messages for invalid inputs, zero division, and overflow errors.
- **Responsive UI**: Adjusts the size of the window and buttons based on the content.
- **Custom Styling**: Uses `qdarkstyle` for a dark theme and additional custom styles for buttons.

### Project Structure

- **main.py**: The entry point of the application. It sets up the main window, display, info label, and buttons grid.
- **main_window.py**: Defines the `MainWindow` class, which is the main container for the application's widgets.
- **display.py**: Defines the `Display` class, a custom `QLineEdit` widget for showing the current input and results.
- **info.py**: Defines the `Info` class, a custom `QLabel` widget for showing additional information.
- **buttons.py**: Defines the `Button` and `ButtonsGrid` classes. `Button` is a custom `QPushButton`, and `ButtonsGrid` manages the layout and functionality of the calculator buttons.
- **utils.py**: Contains utility functions for validating input.
- **styles.py**: Contains the custom styles for the application.
- **variables.py**: Defines constants used throughout the application, such as font sizes and colors.

### How to Run

1. **Clone the repository**:
    ```sh
    git clone <https://github.com/LucasPMartins/Python-Simple-Calculator>
    cd <repository-directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the application**:
    ```sh
    python main.py
    ```

## 🛠 Tools:
![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-0D1117?style=for-the-badge&logo=visual-studio-code&logoColor=007ACC&labelColor=0D1117)&nbsp;
![Git](https://img.shields.io/badge/-Git-0D1117?style=for-the-badge&logo=git&labelColor=0D1117)&nbsp;
![GitHub](https://img.shields.io/badge/-GitHub-0D1117?style=for-the-badge&logo=github&labelColor=0D1117)&nbsp;
![Windows](https://img.shields.io/badge/-Windows-0D1117?style=for-the-badge&logo=windows&logoColor=0a58ee)&nbsp;
![PySide6](https://img.shields.io/badge/PySide6-0D1117?style=for-the-badge&logo=qt&logoColor=41CD52)&nbsp;

## 👨‍💻 Programming Language
![Python](https://img.shields.io/badge/python-0D1117?style=for-the-badge&logo=python&logoColor=ffdd54)

<table>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/2118dd70-3388-49c3-9737-92d305596617" alt="Imagem Maior 1" width="500" />
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/351d5231-4bc5-4ee5-b0df-b8cf70ead461" alt="Imagem Maior 2" width="500" />
    </td>
  </tr>
</table>

<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=1e81b0&height=120&section=footer"/>
