project('infocenter',
          version: '2.3.2',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')
python = import('python')

package_url = 'https://github.com/grouplinuxclient/infocenter/'
contributors = '\n'.join([
    'Jan-Michael Brummer',
    'Malte Borgmann',
                        ])
artists = '\n'.join([
                   ])
application_id = 'de.volkswagen.infocenter'
version = meson.project_version()
copyright = '© 2022 - 2025 Volkswagen AG'

python_bin = python.find_installation('python3')
python_dir = python_bin.get_install_dir()
DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

subdir('data')
subdir('infocenter')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
