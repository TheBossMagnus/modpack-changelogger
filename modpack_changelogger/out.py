def markdown_out(added, removed, updated, old_info, new_info, config, changelog_file):
    style = config["format"]["style"]
    available_styles = {
        "bullet": bullet_list,
        "comma": comma_list,
        "ind_bullet": ind_bullet_list,
        "ind_comma": ind_comma_list,
    }
    markdown_text = []
    markdown_text.append(generate_header(old_info, new_info, config))
    markdown_text = available_styles.get(style, bullet_list)(
        added,
        removed,
        updated,
        markdown_text,
    )

    if changelog_file is None:
        return str(markdown_text)
    write_to_file(changelog_file, markdown_text)


def write_to_file(filename, text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def generate_header(old_info, new_info, config):
    header_format = config["format"]["header"]
    if not header_format["show_header"]:
        return ""

    name = header_format.get("title")
    if name == "auto":
        name = new_info["modpack_name"]

    old_version = (
        f" {old_info['modpack_version']} =>"
        if header_format.get("show_old_version_number")
        else ""
    )
    new_version = (
        f" {new_info['modpack_version']}"
        if header_format.get("show_new_version_number")
        else ""
    )

    return f"{'#' * header_format['size']} {name}{old_version}{new_version}\n"


def bullet_list(added, removed, updated, markdown_text):
    if added:
        markdown_text.extend(["### Added:"] + [f"- {mod}" for mod in added])
    if removed:
        markdown_text.extend(["### Removed:"] + [f"- {mod}" for mod in removed])
    if updated:
        markdown_text.extend(["### Updated:"] + [f"- {mod}" for mod in updated])

    return "\n".join(markdown_text)


def comma_list(added, removed, updated, markdown_text):
    if added:
        markdown_text.append("- Added: " + ", ".join(f"{mod}" for mod in added))
    if removed:
        markdown_text.append("- Removed: " + ", ".join(f"{mod}" for mod in removed))
    if updated:
        markdown_text.append("- Updated: " + ", ".join(f"{mod}" for mod in updated))

    return "\n".join(markdown_text)


def ind_bullet_list(added, removed, updated, markdown_text):
    if added:
        markdown_text.extend(f"- Added {mod}" for mod in added)
    if removed:
        markdown_text.extend(f"- Removed {mod}" for mod in removed)
    if updated:
        markdown_text.extend(f"- Updated {mod}" for mod in updated)

    return "\n".join(markdown_text)


def ind_comma_list(added, removed, updated, markdown_text):
    markdown_text.append("**Changes:**")

    if added:
        markdown_text.append(", ".join(f"Added {mod}" for mod in added))
    if removed:
        markdown_text.append(", ".join(f"Removed {mod}" for mod in removed))
    if updated:
        markdown_text.append(", ".join(f"Updated {mod}" for mod in updated))

    return " ".join(markdown_text)
