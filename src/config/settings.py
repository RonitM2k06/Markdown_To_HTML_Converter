import json
from dataclasses import dataclass, asdict
from pathlib import Path
from loguru import logger

SETTINGS_FILE = Path.home() / ".markdowntohtml_settings.json"


@dataclass
class AppSettings:
    theme: str = "light"
    font_family: str = "sans-serif"
    font_size: int = 14

    @classmethod
    def load(cls) -> "AppSettings":
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"Loaded settings from {SETTINGS_FILE}")
                return cls(**data)
            except Exception as e:
                logger.error(f"Failed to load settings: {e}")
        return cls()

    def save(self) -> None:
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(asdict(self), f, indent=4)
            logger.info(f"Saved settings to {SETTINGS_FILE}")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
