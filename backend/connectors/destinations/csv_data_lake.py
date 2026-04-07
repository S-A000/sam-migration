import pandas as pd
import os
from connectors.base import BaseDestination

class CSVConnector(BaseDestination):
    def __init__(self, config):
        self.file_path = config['path']

    def load(self, data):
        df = pd.DataFrame(data)
        # Agar file pehle se hai toh header mat likho, sirf append karo
        file_exists = os.path.isfile(self.file_path)
        df.to_csv(self.file_path, mode='a', index=False, header=not file_exists)
        return True