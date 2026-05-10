import sys
import os

# 1. This tells the system where your code is hiding
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# 2. This imports your EXACT 'demo' from your original file
from qatalyst.ui.gradio_app import demo

if __name__ == "__main__":
    # 3. This launches your 'demo' exactly as you designed it
    demo.launch()
