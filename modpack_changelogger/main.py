from .compare_packs import compare_packs
from .config_handler import load_config
from .extract_pack_data import cf_get_pack_data, mr_get_pack_data
from .get_json import get_json
from .out import markdown_out
from .overrides_detection import add_overrides


def generate_changelog(old_path, new_path, config_path, changelog_file):
    # Load config
    config = load_config(config_path)

    # Parse the json files
    MODPACKS_FORMAT, old_json, old_config_hash, old_script_hash, old_overrides = (
        get_json(None, old_path)
    )  # None because that the format is not yet known, it will be whatever detected by the function
    MODPACKS_FORMAT, new_json, new_config_hash, new_script_hash, new_overrides = (
        get_json(MODPACKS_FORMAT, new_path)
    )  # The format of the first pack is now known, so the function checks it is the same as the second one

    # Get pack data based on the modpack format
    if MODPACKS_FORMAT == "modrinth":
        old_ids, new_ids, old_info, new_info = mr_get_pack_data(old_json, new_json)
    else:
        old_ids, new_ids, old_info, new_info = cf_get_pack_data(old_json, new_json)
    if (
        config["check"]["identified_overrides_mods"]
        or config["check"]["unidentified_overrides_mods"]
    ):
        (
            old_identified_overrides,
            new_identified_overrides,
            old_unidentified_overrides,
            new_unidentified_overrides,
        ) = add_overrides(MODPACKS_FORMAT, old_overrides, new_overrides, config)
        old_ids = old_ids.union(old_identified_overrides)
        new_ids = new_ids.union(new_identified_overrides)

    # Compare the packs
    added, removed, updated = compare_packs(
        MODPACKS_FORMAT,
        old_ids,
        new_ids,
        old_info,
        new_info,
        old_config_hash,
        new_config_hash,
        old_script_hash,
        new_script_hash,
        config,
    )
    if config["check"]["unidentified_overrides_mods"]:
        added.extend(new_unidentified_overrides)
        removed.extend(old_unidentified_overrides)

    if changelog_file is None:
        changelog_file = "Changelog.md"

    if changelog_file.lower() == "unformatted":
        return added, removed, updated

    if changelog_file.lower() == "formatted":
        return markdown_out(
            added,
            removed,
            updated,
            old_info,
            new_info,
            config,
            None,
        )  # if changelog_file is None, it will return the markdown text

    if changelog_file.lower() == "console":
        print(markdown_out(added, removed, updated, old_info, new_info, config, None))
    else:
        markdown_out(
            added,
            removed,
            updated,
            old_info,
            new_info,
            config,
            changelog_file,
        )
