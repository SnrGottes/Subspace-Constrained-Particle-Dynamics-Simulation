from pathlib import Path
import tomllib
from typing import Any, Dict

class ConfigLoader:
    BASE_DIR = Path(__file__).resolve().parent.parent
    GUI_CONFIG_PATH = BASE_DIR / "config" / "gui_settings.toml"
    SIM_CONFIG_PATH = BASE_DIR / "config" / "sim_settings.toml"
    DEFAULT_SIM_CONFIG_PATH = BASE_DIR / "config" / "default_sim_settings.toml"

    _gui_settings_cache: Dict[str, Any] = {}

    @classmethod
    def get_gui_settings(cls) -> Dict[str, Any]:
        if cls._gui_settings_cache:
            return cls._gui_settings_cache
        if not cls.GUI_CONFIG_PATH.exists():
            raise FileNotFoundError(
                f"Critical error: The UI configuration file was not found at the specified path: {cls.GUI_CONFIG_PATH}"
            )
        with open(cls.GUI_CONFIG_PATH, "rb") as f:
            cls._gui_settings_cache = tomllib.load(f)

        return cls._gui_settings_cache