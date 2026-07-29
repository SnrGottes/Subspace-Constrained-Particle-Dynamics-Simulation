from pathlib import Path
import tomllib
import toml
from typing import Any, Dict

class ConfigLoader:
    BASE_DIR = Path(__file__).resolve().parent.parent
    GUI_CONFIG_PATH = BASE_DIR / "config" / "gui_settings.toml"
    SIM_CONFIG_PATH = BASE_DIR / "config" / "sim_settings.toml"

    _gui_settings_cache: Dict[str, Any] = {}
    _sim_settings_cache: Dict[str, Any] = {}

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

    @classmethod
    def get_sim_settings(cls) -> Dict[str, Any]:
        if cls._sim_settings_cache:
            return cls._sim_settings_cache
        if not cls.SIM_CONFIG_PATH.exists():
            raise FileNotFoundError(
                f"Critical error: The UI configuration file was not found at the specified path: {cls.SIM_CONFIG_PATH}"
            )
        with open(cls.SIM_CONFIG_PATH, "rb") as f:
            cls._sim_settings_cache = tomllib.load(f)
    
        return cls._sim_settings_cache

    @staticmethod
    def update_sim_settings(new_settings: dict, file_path: str = "config/sim_settings.toml") -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            toml.dump(new_settings, f)