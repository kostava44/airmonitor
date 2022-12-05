import aioesphomeapi
import asyncio
import os


async def main():
    """Connect to an ESPHome device and get details."""

    # Establish connection
    api = aioesphomeapi.APIClient(
        "airmonitor.local",
        6053,
        os.environment["ESPHOME_API_PASSWORD"],
        noise_psk=os.environment["ESPHOME_API_KEY"],
    )
    await api.connect(login=True)

    # Get API version of the device's firmware
    print(api.api_version)

    # List all entities of the device
    entities = await api.list_entities_services()
    print(entities)

    sensors, services = await api.list_entities_services()
    await api.execute_service(services[0], {})


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
