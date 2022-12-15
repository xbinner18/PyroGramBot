""" The core 'pyrobot' module"""

import os
from importlib import import_module, reload
from pathlib import Path
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers.handler import Handler
from pyrobot import (
    COMMAND_HAND_LER,
    LOGGER
)
from pyrobot.helper_functions.cust_p_filters import sudo_filter


@Client.on_message(
    filters.command(["load", "install"], COMMAND_HAND_LER)  &
    sudo_filter
)
async def load_plugin(client: Client, message: Message):
    """ load TG Plugins """
    status_message = await message.reply("...")
    try:
        if message.reply_to_message is not None:
            down_loaded_plugin_name = await message.reply_to_message.download(
                file_name="./plugins/"
            )
            if down_loaded_plugin_name is not None:
                # LOGGER.info(down_loaded_plugin_name)
                relative_path_for_dlpn = os.path.relpath(
                    down_loaded_plugin_name,
                    os.getcwd()
                )
                # LOGGER.info(relative_path_for_dlpn)
                lded_count = 0
                path = Path(relative_path_for_dlpn)
                module_path = ".".join(
                    path.parent.parts + (path.stem,)
                )
                # LOGGER.info(module_path)
                module = reload(import_module(module_path))
                # https://git.io/JvlNL
                for name in vars(module):
                    # noinspection PyBroadException
                    try:
                        handler, group = getattr(module, name).handler

                        if isinstance(handler, Handler) and isinstance(group, int):
                            client.add_handler(handler, group)
                            LOGGER.info(
                                f'[{client.session_name}] [LOAD] {type(handler).__name__}("{name}") in group {group} from "{module_path}"'
                            )

                            lded_count += 1
                    except Exception:
                        pass
                await status_message.edit(
                    f"installed {lded_count} commands / plugins"
                )
    except Exception as error:
        await status_message.edit(
            f"ERROR: <code>{error}</code>"
        )
