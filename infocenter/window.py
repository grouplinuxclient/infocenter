# SPDX-License-Identifier: GPL-2.0-or-later

import getpass
import gi
import socket

import yaml

from gettext import gettext as _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, GLib, Gtk  # noqa E402

from infocenter.action_row import ActionRow  # noqa E402
from infocenter.disclaimer import Disclaimer  # noqa E402
from infocenter.quicklink import QuickLink  # noqa E402
from infocenter import system_check, system_information_provider  # noqa E402

from pathlib import Path  # noqa E402


@Gtk.Template(resource_path="/de/volkswagen/infocenter/gtk/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    LANG_PREFIX = system_information_provider.get_language_short_code()
    BASE_YAML = "/de/volkswagen/infocenter/yaml"
    RELATIVE_AUTOSTART_FILE_PATH = ".config/infocenter/do_not_start_file"

    stack = Gtk.Template.Child()
    flowbox = Gtk.Template.Child()

    ehd_preferences_group = Gtk.Template.Child()

    mail_action_row = Gtk.Template.Child()
    mail_link_button = Gtk.Template.Child()

    phone_action_row = Gtk.Template.Child()
    phone_link_button = Gtk.Template.Child()

    # System Information
    system_information_preferences_group = Gtk.Template.Child()
    computer_name_action_row = Gtk.Template.Child()
    fqdn_action_row = Gtk.Template.Child()
    user_name_action_row = Gtk.Template.Child()
    os_action_row = Gtk.Template.Child()
    hardware_model_action_row = Gtk.Template.Child()
    chassis_asset_tag_action_row = Gtk.Template.Child()
    bios_action_row = Gtk.Template.Child()
    cpu_action_row = Gtk.Template.Child()
    kernel_action_row = Gtk.Template.Child()

    # Client Information
    client_preferences_group = Gtk.Template.Child()

    # Disclaimer
    disclaimer_text_box = Gtk.Template.Child()
    autostart_checkbutton = Gtk.Template.Child()

    # Checks
    zscaler_service_label = Gtk.Template.Child()
    proxy_port_label = Gtk.Template.Child()
    pac_file_label = Gtk.Template.Child()
    vpn_label = Gtk.Template.Child()

   def add_quicklinks(self):
        """
        Displays the configured quick actions in top flowbox.
        Configured in: /yaml/quicklinks.yaml
        """
        resource = self.get_language_resource("quicklinks.yaml")
        if not resource:
            return
 
        quicklinks_yml = yaml.safe_load(resource.get_data())
        if not quicklinks_yml:
          self.quicklinks_group.set_visible(False)
          return
 
        for entry in quicklinks_yml:
            self.flowbox.append(QuickLink(entry["uri"], entry["title"], entry["icon"]))

    def add_ehd(self):
        """
        Adds support contacts.
        Configured in: /yaml/support.yaml
        """

        resource = self.get_language_resource("support.yaml")
        if not resource:
            return

        quicklinks_yml = yaml.safe_load(resource.get_data())

        self.ehd_preferences_group.set_title(quicklinks_yml["title"])

        self.mail_action_row.set_subtitle(quicklinks_yml["mail"])
        self.phone_action_row.set_subtitle(quicklinks_yml["phone"])

        self.mail_link_button.set_uri("mailto:" + quicklinks_yml["mail"])
        self.phone_link_button.set_uri("tel:" + quicklinks_yml["phone"])

    def add_system_information(self):
        """
        Adds System Information and provides an overview over system internals like
            - hostname
            - fqdn
            - os
            - hardware model
            - bios version
            - cpu model
            - kernel version
            - List of attached monitors (not working at the moment)
        """

        self.computer_name_action_row.set_subtitle(socket.gethostname().upper())  # noqa: E501
        self.fqdn_action_row.set_subtitle(socket.getfqdn().upper())  # noqa: E501
        self.user_name_action_row.set_subtitle(getpass.getuser().upper())  # noqa: E501
        self.os_action_row.set_subtitle(system_information_provider.get_os())  # noqa: E501
        self.hardware_model_action_row.set_subtitle(
            system_information_provider.get_hardware_model()
        )  # noqa: E501
        self.chassis_asset_tag_action_row.set_subtitle(
            system_information_provider.get_chassis_asset()
        )  # noqa: E501
        self.bios_action_row.set_subtitle(
            system_information_provider.get_bios_version()
        )  # noqa: E501
        self.cpu_action_row.set_subtitle(system_information_provider.get_cpu_model())  # noqa: E501
        self.kernel_action_row.set_subtitle(
            system_information_provider.get_kernel_version()
        )  # noqa: E501

        for index, monitor in enumerate(system_information_provider.get_monitor_list()):
            self.system_information_preferences_group.add(
                ActionRow("Monitor " + str(index), monitor[0])
            )

        for index, card in enumerate(
            system_information_provider.get_graphic_card_list()
        ):
            self.system_information_preferences_group.add(
                ActionRow("Graphic Card " + str(index), card)
            )

    def add_client_information(self):
        """
        Adds Client Information and provides an overview over the business client.
        Configured in: /yaml/client.yaml
        """

        resource = self.get_language_resource("client.yaml")
        if not resource:
            return

        client_yml = yaml.safe_load(resource.get_data())
        if not client_yml:
            return

        self.client_preferences_group.set_title(client_yml["title"])

        for entry in client_yml["client"]:
            self.client_preferences_group.add(
                ActionRow(
                    entry["label"],
                    self._machine_info.get(entry["value"]) or "(not set)",
                )
            )

    def add_disclaimer(self):
        """
        Adds disclaimer and legal guidelines.
        Configured in: /yaml/disclaimer.yaml
        """
        resource = self.get_language_resource("disclaimer.yaml")
        if not resource:
            return

        disclaimer_yml = yaml.safe_load(resource.get_data())
        for entry in disclaimer_yml:
            self.disclaimer_text_box.append(
                Disclaimer(
                    GLib.markup_escape_text(entry["title"]),
                    GLib.markup_escape_text(entry["body"]),
                )
            )

        do_not_start_file = Path.joinpath(
            Path.home(), self.RELATIVE_AUTOSTART_FILE_PATH
        )

        if not do_not_start_file.is_file():
            self.stack.set_visible_child_name("disclaimer")
            self.autostart_checkbutton.set_visible(True)

    def add_tests(self):
        """
        Calls system checks and displays the result in the corresponding test entry
        """
        proxy = system_check.check_local_proxy_port()
        self.set_test_value(self.proxy_port_label, proxy)

        pac = system_check.check_pac_file()
        self.set_test_value(self.pac_file_label, pac)

        zscaler = system_check.check_zscaler_service()
        self.set_test_value(self.zscaler_service_label, zscaler)

        vpn = system_check.check_vpn()
        self.set_test_value(self.vpn_label, vpn)

    def set_test_value(self, label, value):
        """
        Args:
            label (Adw.Label): Adwaita widget, whose text and CSS class is set
            value (bool): Test-Value, which will be interpreted as successful or failed
        """
        if value:
            label.set_label(_("Success"))
            label.add_css_class("success")
        else:
            label.set_label(_("Failed"))
            label.add_css_class("error")

    def _load_machine_info(self):
        try:
            with open("/etc/machine-info") as machine_info:
                for line in machine_info:
                    try:
                        key, value = line.rstrip().split("=")

                        self._machine_info[key] = value.replace('"', "")
                    except ValueError:
                        pass
        except FileNotFoundError:
            pass

    def get_language_resource(self, file_name: str) -> Gio.Resource:
        """
        Returns Gio loaded resources from yaml filename.
        Will fallback to english if language is not available.

        Args:
            file_name (str): yaml filename
        """

        file_path = "{0}/{1}/{2}".format(self.BASE_YAML, self.LANG_PREFIX, file_name)
        fallback_path = "{0}/en/{1}".format(self.BASE_YAML, file_name)
        try:
            return Gio.resources_lookup_data(
                file_path,
                Gio.ResourceLookupFlags.NONE,
            )
        except GLib.GError:
            return Gio.resources_lookup_data(
                fallback_path,
                Gio.ResourceLookupFlags.NONE,
            )

    @Gtk.Template.Callback()
    def on_autostart_checkbutton(self, widget):
        do_not_start_file = Path.joinpath(
            Path.home(), Window.RELATIVE_AUTOSTART_FILE_PATH
        )

        do_not_start_file.touch()
        if do_not_start_file.is_file():
            widget.set_visible(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._machine_info = {}
        self._load_machine_info()

        self.add_quicklinks()
        self.add_ehd()
        self.add_system_information()
        self.add_client_information()
        self.add_disclaimer()
        self.add_tests()
