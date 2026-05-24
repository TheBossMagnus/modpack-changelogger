import asyncio
import json

import aiohttp

from .utils import CF_API_URL, CF_HEADERS, MR_API_URL, MR_HEADERS


async def get_mod_names(MODPACKS_FORMAT, added_ids, removed_ids, updated_ids):
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=15),
    ) as session:
        api_function = {
            "modrinth": request_from_mr_api,
            "curseforge": request_from_cf_api,
        }.get(MODPACKS_FORMAT)
        added_names, removed_names, updated_names = await asyncio.gather(
            api_function(session, added_ids),
            api_function(session, removed_ids),
            api_function(session, updated_ids),
        )

    return added_names, removed_names, updated_names


async def request_from_mr_api(session, ids):
    if not ids:
        return []

    names = []
    url = f"{MR_API_URL}/projects?ids={json.dumps(list(ids))}"

    async with session.get(url, headers=MR_HEADERS) as response:
        response.raise_for_status()
        data = await response.json()
        names = [project.get("title") for project in data]
    return names


async def request_from_cf_api(session, ids):
    if not ids:
        return []

    names = []
    url = f"{CF_API_URL}v1/mods"

    async with session.post(
        url,
        headers=CF_HEADERS,
        json={"modIds": list(ids)},
    ) as response:
        data = await response.json()
        names = [project["name"] for project in data["data"]]
    return names
