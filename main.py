import sys
import os
import logging
from pathlib import Path

src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def setup_environment():
    """Setup application environment"""

    directories = ['logs', 'cache', 'data']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def setup_logging():
    """Setup application logging configuration"""

    log_file = Path('logs') / 'application.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main application entry point"""

    try:
        setup_environment()
        setup_logging()

    except ImportError as e:
        print(f"Import Error: {e}")

    except Exception as e:
        print(f"Application Error: {e}")

if __name__ == "__main__":
    main()