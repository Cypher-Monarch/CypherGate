# Settings

CypherGate stores user settings in:

```text
~/.config/cyphergate/settings.json
```

If the file does not exist, it is created using the application's default
configuration. Missing settings are also populated from the defaults.

Settings are grouped into:

* `theme`
* `icons`
* `widgets`
* `table`
* `application`
* `vpn`

Changes to supported settings are detected automatically and applied without
restarting CypherGate.

## `theme`

Controls the application's Qt stylesheet.

| Setting            | Type        | Description                                       |
| ------------------ | ----------- | ------------------------------------------------- |
| `mode`             | string      | `builtin` or `custom`                             |
| `name`             | string      | Name of a builtin theme                           |
| `path`             | string/null | Path to a custom `.qss` theme                     |

For a builtin theme:

```json
{
  "theme": {
    "mode": "builtin",
    "name": "playful",
    "path": null
  }
}
```

For a custom theme:

```json
{
  "theme": {
    "mode": "custom",
    "name": null,
    "path": "/path/to/theme.qss"
  }
}
```

## `icons`

Controls icon appearance.

### `icons.size`

Sets the size of individual icons. The `tray` subsection controls the
corresponding system-tray menu icons.

### `icons.color`

Sets the color of individual icons. Colors use Qt-compatible color strings,
such as `#FFD700`. The `tray` subsection controls system-tray menu icons.

## `widgets`

### `widgets.spinner`

Controls the connection spinner.

| Setting          | Type    | Description                          |
| ---------------- | ------- | ------------------------------------ |
| `size`           | integer | Spinner size in pixels               |
| `color`          | string  | Spinner color                        |
| `thickness`      | integer | Spinner stroke width                 |
| `fps`            | integer | Animation update rate                |
| `rotation_speed` | number  | Rotation speed in degrees per second |

### `widgets.table`

Controls which server metadata is displayed and how servers are sorted.

```json
{
  "table": {
    "columns": [
      "country",
      "ping",
      "speed",
      "users"
    ],
    "sort_by": "ping",
    "sort_order": "ascending"
  }
}
```

#### `columns`

A list of server fields to display, in the order they should appear.

Supported fields are:

* `country`
* `ping`
* `speed`
* `users`
* `hostname`
* `ip`
* `country_short`
* `score`

_Columns can be reordered or repeated._

#### `sort_by`

The server field used for sorting.

#### `sort_order`

Either `ascending` or `descending`.

## `application`

Controls general application behavior.

| Setting                  | Type    | Description                                                            |
| ------------------------ | ------- | ---------------------------------------------------------------------- |
| `minimize_to_tray`       | boolean | Whether closing/minimizing the application sends it to the system tray |
| `notifications`          | boolean | Enables or disables desktop notifications                              |
| `status_update_interval` | integer | Interval, in milliseconds, at which the GUI polls daemon status        |
| `use_custom_fonts`       | boolean | Allow loading of fonts not installed system-wide                       | 

_builtin theme pastel-orange requires value of `use_custom_fonts` to be set to `true` to get the complete theme experience_


## `vpn`

Controls VPN connection behavior.

| Setting              | Type        | Description                                                                                 |
| -------------------- | ----------- | ------------------------------------------------------------------------------------------- |
| `connection_timeout` | integer     | Maximum time, in seconds, to wait for a connection                                          |
| `default_country`    | string/null | Country selected after server data is loaded; `null` leaves the default selection unchanged |

`default_country` uses the full country name reported by VPNGate, for example:

```json
"default_country": "Japan"
```

Set it to `null` to disable the default country.

## Hot reload

Changes to the settings file are detected automatically.

The following settings can be applied without restarting:

* themes;
* icon sizes and colors;
* tray icon appearance;
* spinner settings;
* table columns and sorting.

Settings affecting application or VPN behavior are read by the relevant
runtime component when they are used.

## Configuration version

The `config_version` field identifies the settings schema version.

```json
"config_version": 1
```

This value is reserved for future configuration migrations.
