# kasa_helper.py

import asyncio
from kasa import Discover, SmartPlug

class KasaHelper:
    def __init__(self):
        # Create a new event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.plugs = {}
        self.discover_plugs()

    def discover_plugs(self):
        """Discover all Kasa smart plugs on the network."""
        self.loop.run_until_complete(self._discover_plugs())

    async def _discover_plugs(self):
        devices = await Discover.discover()
        for addr, dev in devices.items():
            if dev.is_plug:
                plug = SmartPlug(addr)
                await plug.update()
                self.plugs[addr] = plug  # Use IP address as the key

    def update_all_plugs(self):
        """Update the status of all plugs."""
        self.loop.run_until_complete(self._update_all_plugs())

    async def _update_all_plugs(self):
        tasks = [plug.update() for plug in self.plugs.values()]
        await asyncio.gather(*tasks)

    def get_all_plug_states(self):
        """Get the on/off state of all plugs."""
        self.update_all_plugs()
        plug_states = {}
        for addr, plug in self.plugs.items():
            plug_states[addr] = {
                'alias': plug.alias,
                'is_on': plug.is_on
            }
        return plug_states

    def turn_on_plug(self, ip):
        """Turn on a specific plug by its IP address."""
        plug = self.plugs.get(ip)
        if plug:
            return self.loop.run_until_complete(plug.turn_on())

    def turn_off_plug(self, ip):
        """Turn off a specific plug by its IP address."""
        plug = self.plugs.get(ip)
        if plug:
            return self.loop.run_until_complete(plug.turn_off())
        
    def rename_plug(self, ip, new_alias):
        """Rename a specific plug by its IP address."""
        plug = self.plugs.get(ip)
        if plug:
            return self.loop.run_until_complete(self._rename_plug(plug, new_alias))

    async def _rename_plug(self, plug, new_alias):
        await plug.set_alias(new_alias)
        await plug.update()  # Update the plug's information
