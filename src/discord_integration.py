import requests
import json

people = set()
api_base = "https://discord.com/api/v9"

with open("discordauth.txt") as f:
    auth = f.read()

headers = {
    "authorization": f"{auth}"
}


def get_messages(channel_id: int, limit: int = 100) -> list:
    """
    Returns messages from a given channel.
    Args:
        channel_id (int): The channel ID to request from
        limit (int): Amount of messages to request

    Returns:
        list: Messages from the specified channel.

    """
    r = requests.get(f"{api_base}/channels/{channel_id}/messages?limit={limit}", headers=headers)
    jsonn = json.loads(r.text)
    new_list = []
    for value in jsonn:
        if not value["content"]:
            people.add(value["author"]["global_name"])
            new_list.append(
                {"username": value["author"]["global_name"], "content": "[(call/image/other)]", "id": value["id"]})
        else:
            people.add(value["author"]["global_name"])
            new_list.append(
                {"username": value["author"]["global_name"], "content": value["content"], "id": value["id"]})

    # Reverse the list of messages
    new_list.reverse()
    return new_list


def send_message(msg, channel) -> None:
    """
    Sends a message to a given channel.
    Args:
        msg (str): Message
        channel (int): The channel to send the message

    Returns:
        None: Nothing

    """
    r = requests.post(f"{api_base}/channels/{channel}/messages",
                      headers=headers,
                      json={"content": msg})
    # print(r.text)


def get_friends() -> dict:
    """
    Returns a list of friends for the current account.
    Returns:
        dict: Friends of the current account
    """
    r = requests.get(f"{api_base}/users/@me/relationships",
                     headers=headers)

    # for friend in r.json():
    #     print(friend["user"]["global_name"])

    return r.json()


def get_channel_from_id(user_id: int) -> int:
    """
    Converts a user ID into a channel ID.
    Args:
        user_id (int): The user's ID

    Returns:
        int: The user's channel which they can be reached
    """
    r = requests.post(f"{api_base}/users/@me/channels",
                      headers=headers, json={"recipient_id": user_id})
    return r.json()["id"]


def get_guilds() -> dict:
    """
    Returns all guilds (aka servers) that the current user is in.
    Returns:
        dict: Guilds that the current account is in.
    """

    r = requests.get(f"{api_base}/users/@me/guilds",
                     headers=headers)

    # You can get the icon of the server by: https://cdn.discordapp.com/icons/{id}/{icon_name}.
    # You get the rest of the info from this function.
    return r.json()


def get_guild_channels(guild_id: int) -> dict:
    """
    Returns all channels in a guild.
    Args:
        guild_id (int): Any guild that the current user is in.

    Returns:
        dict: The channels in the guild.
    """

    r = requests.get(f"{api_base}/guilds/{guild_id}/channels",
                     headers=headers)

    return r.json()
