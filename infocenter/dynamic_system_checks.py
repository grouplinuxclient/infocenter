# SPDX-License-Identifier: GPL-2.0-or-later
import importlib
import json
import os


class Dynamic_checks:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "checks_config.json")
        self.plugins_configs = self._load_config()

    def _load_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                plugins = cfg.get("plugins", [])
                return [p for p in plugins if p.get("enabled", False)]
        except Exception as e:
            print("ERROR reading config:", e)
            return []

    def generate_display_name(self, plugin_id: str) -> str:
        return plugin_id.replace("_", " ").title()

    def load_plugin(self, plugin_id: str):
        module_name = f"infocenter.plugins.{plugin_id}_plugin"
        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError:
            print(f"PLUGIN NOT FOUND: {module_name}.py")
            return None
        except Exception as e:
            print(f"ERROR loading plugin {module_name}: {e}")
            return None

    def render(self, preference_page, set_test_value):
        for plugin in self.plugins_configs:
            plugin_id = plugin.get("id")

            plugin_module = self.load_plugin(plugin_id)
            if not plugin_module:
                continue

            display_name = getattr(
                plugin_module, "DISPLAY_NAME", None
            ) or self.generate_display_name(plugin_id)

            if hasattr(plugin_module, "add_to_preferences_page"):
                try:
                    plugin_module.add_to_preferences_page(
                        preference_page,
                        set_test_value,
                        display_name=display_name,
                    )
                except Exception as e:
                    print(f"ERROR rendering plugin UI for {plugin_id}: {e}")
            else:
                print(f"PLUGIN HAS NO UI: {plugin_id}")
