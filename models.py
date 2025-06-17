from dataclasses import dataclass

@dataclass
class Update:
    email: str
    text: str
    image_path: str = None