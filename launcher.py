import subprocess
import time

# Actual Medical Wholesale App project folder
project_folder = r"C:\Users\lappify\Desktop\Python\projects\Medical_store\Medical_Wholesale_App"

# Python from your working virtual environment
python_exe = r"C:\Users\lappify\Desktop\Python\.venv\Scripts\python.exe"

# Main Streamlit application
app_file = project_folder + r"\app.py"

# Start Streamlit
subprocess.Popen(
    [
        python_exe,
        "-m",
        "streamlit",
        "run",
        app_file,
        "--server.headless",
        "false",
        "--browser.gatherUsageStats",
        "false"
    ],
    cwd=project_folder
)

time.sleep(2)