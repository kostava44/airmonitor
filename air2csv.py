#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(p: with p; [ aioesphomeapi ])"
import csv
import datetime
import logging
import aioesphomeapi
import asyncio
import zeroconf


async def main(csvw):
    api = aioesphomeapi.APIClient(
        "airmonitor.local",
        6053,
        os.environment["ESPHOME_API_PASSWORD"],
        noise_psk=os.environment["ESPHOME_API_KEY"],
    )

    await api.connect(login=True)

    sensors, _ = await api.list_entities_services()
    sensor_by_keys = dict((sensor.key, sensor.name) for sensor in sensors)

    await api.disconnect()

    def cb(state):
        if type(state) == aioesphomeapi.SensorState:
            csvw.writerow(
                [datetime.datetime.now(), sensor_by_keys[state.key], state.state]
            )

    async def on_connect() -> None:
        try:
            await api.subscribe_states(cb)
        except APIConnectionError:
            await cli.disconnect()

    async def on_disconnect() -> None:
        logging.warning("disconnected")

    logic = aioesphomeapi.ReconnectLogic(
        client=api,
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        zeroconf_instance=zeroconf.Zeroconf(),
    )
    await logic.start()

    try:
        await asyncio.Event().wait()  # sleep
    except:
        await logic.stop()


with open("air.csv", "a", newline="") as csvf:
    csvw = csv.writer(csvf)

    asyncio.run(main(csvw))
