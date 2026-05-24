import asyncio

from .get_mod_names import get_mod_names


def compare_packs(
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
):
    updated_ids = old_ids & new_ids
    added_ids = new_ids - old_ids
    removed_ids = old_ids - new_ids

    # Remove a category if disabled in config
    added_ids = added_ids if config["check"]["added_mods"] else set()
    removed_ids = removed_ids if config["check"]["removed_mods"] else set()
    updated_ids = updated_ids if config["check"]["updated_mods"] else set()

    added_mods, removed_mods, updated_mods = asyncio.run(
        get_mod_names(MODPACKS_FORMAT, added_ids, removed_ids, updated_ids),
    )

    added_mods = sorted(mod for mod in added_mods if mod)
    removed_mods = sorted(mod for mod in removed_mods if mod)
    updated_mods = sorted(mod for mod in updated_mods if mod)

    if config["check"]["loader"]:
        if old_info["loader"] != new_info["loader"]:
            added_mods.append(f"{new_info['loader'].capitalize()} (mod loader)")
            removed_mods.append(f"{old_info['loader'].capitalize()} (mod loader)")

        elif old_info["loader_version"] != new_info["loader_version"]:
            updated_mods.append(f"{new_info['loader'].capitalize()} (mod loader)")

    if (
        config["check"]["mc_version"]
        and old_info["mc_version"] != new_info["mc_version"]
    ):
        updated_mods.append(f"Minecraft version to {new_info['mc_version']}")

    if config["check"]["config"] and old_config_hash != new_config_hash:
        updated_mods.append("Mods configs")

    if config["check"]["script"] and old_script_hash != new_script_hash:
        updated_mods.append("CraftTweaker scripts")

    return added_mods, removed_mods, updated_mods
