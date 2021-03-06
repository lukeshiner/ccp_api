"""API credentials and setting management."""

from pathlib import Path

import yaml


class CredentialsFile:
    """Wrapper for the .ccp_credentials.yaml file."""

    CREDENTIALS_FILE_NAME = ".ccp_credentials.yaml"

    def find(self, directory=None):
        """Return the path of a Pipfile in parent directories."""
        if directory is None:
            directory = Path.cwd()
        filepath = directory.joinpath(self.CREDENTIALS_FILE_NAME)
        if filepath.exists():
            return filepath
        elif directory.match(directory.root):  # Directory is the root directory
            return None
        else:
            return self.find(directory=directory.parent)

    def load(self):
        """Read API credentials from file."""
        file_path = self.find()
        with open(str(file_path), "r") as f:
            config = yaml.load(f.read())
        return config["brand_id"], config["security_hash"]


class Credentials:
    """API credentials and settings manager."""

    class __Credentials:
        def __init__(self):
            self.reset()

        def reset(self):
            self.brand_id = None
            self.security_hash = None
            self.raw_response = False

        def set(self, brand_id=None, security_hash=None):
            """Set Cloud Commerce Pro API credentials."""
            if brand_id is None and security_hash is None:
                brand_id, security_hash = self.get_from_file()
            self.brand_id = brand_id
            self.security_hash = security_hash

        def get_from_file(self):
            """Set Cloud Commerce Pro API credentials from a .ccp_credentials.yaml file."""
            self.credentials_file = CredentialsFile()
            return self.credentials_file.load()

    instance = None

    def __init__(self):
        """Create a __Credentials instance if one does not exist."""
        if not Credentials.instance:
            Credentials.instance = Credentials.__Credentials()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
