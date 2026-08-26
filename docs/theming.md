# Theming

CypherGate uses Qt Style Sheets (QSS) for application theming.

A theme is a `.qss` stylesheet that controls the visual appearance of the
application's widgets.

## Theme selection

Theme selection is configured through `settings.json`.

### Builtin themes

Builtin themes are stored in the application's theme directory.

```json
{
  "theme": {
    "mode": "builtin",
    "name": "playful",
    "path": null
  }
}
````

When `mode` is `builtin`, CypherGate loads:

```text
<theme directory>/<name>.qss
```

During development, builtin themes are loaded from the repository's `themes/`
directory.

Installed/frozen builds load builtin themes from:

```text
/usr/share/cyphergate/themes
```

### Custom themes

Custom themes can be loaded from an arbitrary `.qss` file:

```json
{
  "theme": {
    "mode": "custom",
    "name": null,
    "path": "/path/to/theme.qss"
  }
}
```

When `mode` is `custom`, the configured `path` is used directly.

If the resolved theme file does not exist, CypherGate uses its builtin fallback
stylesheet instead.

## QSS

CypherGate themes use standard Qt Style Sheet syntax.

A stylesheet can target widgets by their Qt class:

```qss
QPushButton {
    background-color: #cba6f7;
}
```

or by their CypherGate-specific `objectName`:

```qss
QPushButton#connectButton {
    background-color: #a6e3a1;
}
```

Object names allow individual widgets to be styled without affecting every
widget of the same Qt class.

## Available widgets

### Main window

| Object name    | Widget                  |
| -------------- | ----------------------- |
| `mainWindow`   | Main application window |
| `titleBar`     | Custom title bar        |
| `titleLabel`   | Window title            |
| `headingLabel` | Main heading            |

### Window controls

| Object name      | Widget          |
| ---------------- | --------------- |
| `minimizeButton` | Minimize button |
| `closeButton`    | Close button    |

### VPN controls

| Object name         | Widget              |
| ------------------- | ------------------- |
| `refreshButton`     | Refresh button      |
| `connectButton`     | Connect button      |
| `disconnectButton`  | Disconnect button   |
| `autoConnectButton` | Auto-connect button |
| `cancelButton`      | Cancel button       |

### Server table

| Object name   | Widget                    |
| ------------- | ------------------------- |
| `serverTable` | VPN server table          |
| `animLabel`   | Animated table cell label |

### Country selector

| Object name    | Widget                  |
| -------------- | ----------------------- |
| `countryPopup` | Country selection popup |

## Common selectors

### Buttons

The global `QPushButton` selector can be used to style all buttons:

```qss
QPushButton {
    background-color: #cba6f7;
    color: #11111b;
}
```

Individual buttons can be styled using their object names:

```qss
QPushButton#connectButton {
    background-color: #a6e3a1;
}
```

Button states can also be targeted:

```qss
QPushButton:hover {
    background-color: #b4befe;
}

QPushButton:pressed {
    background-color: #89b4fa;
}

QPushButton:disabled {
    background-color: #45475a;
}
```

### Labels

Labels can be styled globally with `QLabel` or individually using their
object names:

```qss
QLabel {
    color: #cdd6f4;
}

QLabel#headingLabel {
    font-size: 20px;
}
```

### Server table

The server table can be customized using:

```qss
QTableWidget#serverTable
QTableWidget#serverTable::item
QTableWidget#serverTable::item:selected
QHeaderView
QHeaderView::section
QTableCornerButton::section
```

These selectors can be used to customize the table background, cells,
selection, headers, borders, and corner button.

For example:

```qss
QTableWidget#serverTable {
    background-color: #11111b;
    border: 1px solid #313244;
}

QTableWidget#serverTable::item:selected {
    background-color: #cba6f7;
    color: #11111b;
}

QHeaderView::section {
    background-color: #181825;
}
```

### Country selector

The country selector uses a popup frame containing a list view.

The following selectors can be used:

```qss
QFrame#countryPopup
QFrame#countryPopup QListView
QFrame#countryPopup QListView::item
QFrame#countryPopup QListView::item:hover
QFrame#countryPopup QListView::item:selected
```

The popup and its list items can therefore be styled independently.

### Scrollbars

Vertical scrollbars can be styled using:

```qss
QScrollBar:vertical
QScrollBar::handle:vertical
QScrollBar::handle:vertical:hover
```

### Tooltips

Tooltips can be styled globally:

```qss
QToolTip {
    background-color: #181825;
    color: #cdd6f4;
}
```

## States and pseudo-selectors

Qt's standard pseudo-selectors can be used where supported by the target
widget.

Common examples include:

* `:hover`
* `:pressed`
* `:disabled`
* `:selected`

For example:

```qss
QPushButton#connectButton:hover {
    background-color: #b4befe;
}
```

## Hot reload

CypherGate watches the active theme file for changes.

When the active stylesheet changes, CypherGate reloads and reapplies the theme
without requiring an application restart.

Changing the selected theme through `settings.json` is also supported by the
configuration watcher.

Theme reloads are handled separately from the normal icon and widget
configuration reloads.

## Fallback behavior

If the resolved theme path does not exist, CypherGate does not fail to start
because of the missing stylesheet. Instead, the builtin fallback stylesheet is
used.

This applies to both builtin themes whose files cannot be found and custom
themes whose configured paths are invalid.

## Creating a custom theme

A custom theme only needs to be a valid Qt Style Sheet file.

For example:

```qss
QWidget#mainWindow {
    background-color: #101010;
    color: #ffffff;
}

QPushButton {
    background-color: #ffffff;
    color: #101010;
    border: none;
    border-radius: 8px;
}

QPushButton:hover {
    background-color: #cccccc;
}

QTableWidget#serverTable {
    background-color: #101010;
    border: 1px solid #444444;
}

QTableWidget#serverTable::item:selected {
    background-color: #ffffff;
    color: #101010;
}
```

Save the stylesheet as a `.qss` file and point `theme.path` at it:

```json
{
  "theme": {
    "mode": "custom",
    "name": null,
    "path": "/path/to/theme.qss"
  }
}
```

The theme can then be edited while CypherGate is running and the changes will
be picked up by the configuration watcher.

## Qt Style Sheets

CypherGate themes are regular QSS files rather than a separate CypherGate
styling language. Standard Qt Style Sheet selectors and properties supported by
the application's widgets can therefore be used.

This document describes the CypherGate-specific widgets and selectors.
For complete QSS syntax and property behavior, refer to the Qt Style Sheets
documentation.
