import asyncio
import logging

import aiohttp

import constants


def add_overrides(old_overrides, new_overrides, config):

    identical_entries = set(old_overrides.values()) & set(new_overrides.values())
    old_overrides = {hash: name for hash, name in old_overrides.items() if name not in identical_entries}
    new_overrides = {hash: name for hash, name in new_overrides.items() if name not in identical_entries}

    async def get_names_from_hashes(dict1, dict2):
        async with aiohttp.ClientSession() as session:
            for d in [dict1, dict2]:
                for hash, name in list(d.items()): 
                    async with session.get(f"{constants.MR_API_URL}/version_file/{d[hash]}", headers=constants.MR_HEADERS) as response:
                        if response.status == 200:
                            data = await response.json()
                            project_name = data["project_id"]
                            d[project_name] = d.pop(hash)
                            d[project_name] = True
                            logging.debug(f'Found overrides from project id "{project_name}"')
                        else:
                            d[hash] = False

    if constants.Modpacks_Format == "modrinth":
        asyncio.run(get_names_from_hashes(old_overrides, new_overrides))

    old_identified_overrides = {name for name, key in old_overrides.items() if key is True}
    old_unidentified_overrides = {name for name, key in old_overrides.items() if key is False}
    new_identified_overrides = {name for name, key in new_overrides.items() if key is True}
    new_unidentified_overrides = {name for name, key in new_overrides.items() if key is False}

    if config["check"]["identified_overrides_mods"] and not config["check"]["unidentified_overrides_mods"]:
        return old_identified_overrides, new_identified_overrides, {}, {}
    if not config["check"]["identified_overrides_mods"] and config["check"]["unidentified_overrides_mods"]:
        return {}, {}, old_unidentified_overrides, new_unidentified_overrides
    else:
        return old_identified_overrides, new_identified_overrides, old_unidentified_overrides, new_unidentified_overrides
