import asyncio
from datetime import timedelta
from openleadr import OpenADRClient, enable_default_logging
import random

enable_default_logging()

async def collect_report_value():
    # return a fake power meter value for the building
    return round(random.uniform(100, 200))

async def handle_event(event):
    # no logic here to opt out of the event
    return 'optIn'

async def main():
    client = OpenADRClient(ven_name='ven_id_123',
                        vtn_url='https://localhost:8080/OpenADR2/Simple/2.0b',
                        cert='ven_cert.pem',
                        key='ven_key.pem',
                        passphrase='slipstream_openadr_testing',
                        ca_file='ca.crt')

    # Add the report capability to the client
    client.add_report(callback=collect_report_value,
                      resource_id='slipstreams_research_building',
                      measurement='power',
                      sampling_rate=timedelta(seconds=10),
                      report_duration=timedelta(seconds=3600))

    # Add event handling capability to the client
    client.add_handler('on_event', handle_event)

    # Run the client
    await client.run()

# Run the client in the Python AsyncIO Event Loop
loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

