"""API credentials and setting management."""

import os

import yaml


class CredentialsFile:
    """Wrapper for the .ccp_credentials.yaml file."""

    CREDENTIALS_FILE_NAME = ".ccp_credentials.yaml"

    def find(self, directory=None):
        """Return the path of a Pipfile in parent directories."""
        if directory is None:
            directory = os.getcwd()
        if os.path.exists(os.path.join(directory, self.CREDENTIALS_FILE_NAME)):
            return os.path.join(directory, self.CREDENTIALS_FILE_NAME)
        elif os.path.dirname(directory) == directory:
            return None
        else:
            return self.get_wowcher_credentials_file(
                directory=os.path.dirname(directory)
            )

    def load(self):
        """Read API credentials from file."""
        file_path = self.find()
        with open(file_path, "r") as f:
            config = yaml.load(f.read())
        return config["brand_id"], config["security_hash"]


class Credentials:
    """API credentials and settings manager."""

    brand_id = None
    security_hash = None
    raw_response = False

    def set(self, brand_id=None, security_hash=None):
        """Set Cloud Commerce Pro API credentials."""
        if brand_id is None and security_hash is None:
            brand_id, security_hash = self.set_from_file()
        self.brand_id = brand_id
        self.security_hash = security_hash

    def set_from_file(self):
        """Set Cloud Commerce Pro API credentials from a .ccp_credentials.yaml file."""
        self.credentials_file = CredentialsFile()
        return self.credentials_file.load()


login = Credentials()
