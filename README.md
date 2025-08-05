# Information Center

<img align="right" src="./data/icons/hicolor/scalable/apps/de.volkswagen.infocenter.svg" width="10%">

Shows typical disclaimer and offers some quick link for user self support.

## Notes
Custom content can be added in infocenter/yaml/"2 digit-language code"/. Those content files also needs to be added
to the infocenter.gresource.xml file.

### client.yaml
File contains keys which values are read from /etc/machine-info.

### disclaimer.yaml
List of disclaimer text which must be shown to the user.

### quicklinks.yaml
List of URLs which are shown on top of the application.

### support.yaml
Information about how to contact company support (mail/phone).
