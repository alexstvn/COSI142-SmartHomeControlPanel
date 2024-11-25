import asyncio
from kasa import Discover, SmartPlug

async def _discover_smart_plugs():
    """
    Internal function to discover Kasa smart plugs on the local network.
    Returns a list of tuples with device alias and IP address.
    """
    devices = await Discover.discover()
    smart_plugs = []

    for addr, dev in devices.items():
        await dev.update()  # Fetch the device's details
        if dev.is_plug:
            smart_plugs.append((dev.alias, addr))

    return smart_plugs

def discover_smart_plugs():
    """
    Public function to discover smart plugs. Returns a list of smart plugs.
    Each entry is a tuple with (alias, IP address).
    """
    return asyncio.run(_discover_smart_plugs())



async def _control_smart_plug(ip_address, turn_on=True):
    """
    Internal function to control a smart plug.
    Args:
        ip_address (str): The IP address of the smart plug.
        turn_on (bool): Whether to turn the plug on (True) or off (False).
    """
    plug = SmartPlug(ip_address)
    await plug.update()  # Fetch current state

    if turn_on:
        print(f"Turning ON the smart plug at {ip_address}...")
        await plug.turn_on()
    else:
        print(f"Turning OFF the smart plug at {ip_address}...")
        await plug.turn_off()

    print(f"Smart plug at {ip_address} is now {'ON' if turn_on else 'OFF'}.")

def control_smart_plug(ip_address, turn_on=True):
    """
    Public function to control a smart plug.
    Args:
        ip_address (str): The IP address of the smart plug.
        turn_on (bool): Whether to turn the plug on (True) or off (False).
    """
    asyncio.run(_control_smart_plug(ip_address, turn_on))
