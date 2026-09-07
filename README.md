# Modpack Changelogger

**Modpack Changelogger** is a Python tool for comparing two Minecraft modpacks (in `.mrpack` or `.zip` format) and generating a customizable, human-readable changelog in Markdown.

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/TheBossMagnus/modpack-changelogger)


## Features

- **Accurate Modpack Comparison:**  
  Instantly see which mods, resource packs, or files were added, removed, or changed between two modpacks.
- **Minecraft & Modloader Awareness:**  
  Detects changes in Minecraft version, modloaders, configs file and scirpts.
- **Customizable Markdown Output:**  
  Generates a detailed changelog in Markdown, with multiple [output styles](https://github.com/TheBossMagnus/modpack-changelogger/wiki/Configuration#format-section).
- **Configurable:**  
  Supports [custom configuration files](https://github.com/TheBossMagnus/modpack-changelogger/wiki/Configuration) for advanced control over output and comparison.
- **No Python Required for Windows Users:**  
  Download the pre-built `.exe`—no Python installation needed!
- **Use it as a Module:**  
  Easily integrate into your own Python scripts or applications.


---

## Installation

**With pip (recommended):**
```bash
pip install modpack-changelogger
```

**Or download the Windows executable:** 
It does not require having python installed and it's fully portable!
Grab the latest `.exe` from the [releases page](https://github.com/TheBossMagnus/modpack-changelogger/releases/latest).

> [!NOTE] 
> Be aware of petential Windows Defender false positives

[See the wiki for more installation options & details.](https://github.com/TheBossMagnus/modpack-changelogger/wiki/Install-and-run)

---

## Basic Usage

| Option         | Description                                      |
|----------------|--------------------------------------------------|
| `-o`, `--old`  | Path to the original/old modpack file            |
| `-n`, `--new`  | Path to the updated/new modpack file             |
| `-c`, `--config` | (Optional) Path to a configuration file        |
| `-f`, `--file` | Output file for the changelog (`console` for stdout) |

**Example:**  
Compare `old_pack` to `new_pack` using `config.json`, and write the changelog to `output.md`:
```bash
modpack-changelogger -o old_pack.mrpack -n new_pack.mrpack -f output.md
```

**Print changelog to the console:**
```bash
modpack-changelogger -o old_pack.mrpack -n new_pack.mrpack -f console
```

[See the wiki for all command-line options and advanced usage.](https://github.com/TheBossMagnus/modpack-changelogger/wiki/Commands)

## Configuration
You can customize the output format and behavior using a configuration file.
To generate a default configuration file, run:

```bash
modpack-changelogger newconfig #generates a default config file
modpack-changelogger -o old_pack.mrpack -n new_pack.mrpack -c config.json # use said config file
```

[See the wiki for more details on configuration options.](https://github.com/TheBossMagnus/modpack-changelogger/wiki/Configuration)


## Run as a Module
You can also use Modpack Changelogger as a Python module in your own scripts:

```python
from modpack_changelogger import generate_changelog

generate_changelog("old_pack.mrpack", "new_pack.mrpack", "config.json", "output.md")
```

