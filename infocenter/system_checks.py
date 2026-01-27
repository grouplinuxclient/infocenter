# SPDX-License-Identifier: GPL-2.0-or-later
import importlib
import json
import os



def get_config_path():
    return os.path.join(os.path.dirname(__file__), "checks_config.json")

def _load_config(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            plugins = cfg.get("plugins", [])
            return [plugin for plugin in plugins if plugin.get("enabled", False)]
    except Exception as exc:
        print("Error reading config:", exc)
        return []

def load_plugin(plugin_id: str):
    module_name = f"infocenter.plugins.{plugin_id}_plugin"
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        print(f"Plugin not found: {module_name} (ModuleNotFoundError: {exc})")
        return None
    except Exception as exc:
        print(f"Error loading plugin {module_name}: {exc}")
        return None

def create_widgets(plugins_configs, preference_page, set_test_value):
    for plugin in plugins_configs:
        plugin_id = plugin.get("id")

        plugin_module = load_plugin(plugin_id)
        if not plugin_module:
            continue

        if hasattr(plugin_module, "add_to_preferences_page"):
            try:
                plugin_group = plugin_module.add_to_preferences_page(
                    set_test_value,
                )
                preference_page.add(plugin_group)
            except Exception as exc:
                print(f"Error rendering plugin UI for {plugin_id}: {exc}")
        else:
            print(f"PLUGIN HAS NO UI: {plugin_id}")

