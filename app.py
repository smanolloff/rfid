import ConfigParser
from backend import BarcodeProcessor

def main():
    master_config = ConfigParser.ConfigParser()
    master_config.read('config.ini')

    while True:
        data = raw_input()
        processor = BarcodeProcessor(master_config)
        (code, message) = processor.process(data)
        print message + "\n"

if __name__ == '__main__':
    main()
