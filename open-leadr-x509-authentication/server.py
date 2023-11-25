import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRServer, enable_default_logging
from functools import partial

enable_default_logging()

# make dummy event 1 minute into future when server starts
dtstart = datetime.now(timezone.utc) + timedelta(minutes=1)

def ven_lookup(ven_id):
    # Here you define the logic to lookup the VEN by its ID.
    # Since you're testing with a single VEN, you can return its details directly.

    if ven_id == 'ven_id_123':
        return {'ven_id': 'ven_id_123',
                'ven_name': 'MyVEN',
                'fingerprint': '28:36:73:32:53:6C:84:C7:89:95',
                'registration_id': 'reg_id_123'}
    else:
        return None  # Return None if the VEN is not found


async def on_create_party_registration(registration_info):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """
    if registration_info['ven_name'] == 'ven_id_123':
        ven_id = 'ven_id_123'
        registration_id = 'reg_id_123'
        return ven_id, registration_id
    else:
        return False

async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    """
    Inspect a report offering from the VEN and return a callback and sampling interval for receiving the reports.
    """
    callback = partial(on_update_report, ven_id=ven_id, resource_id=resource_id, measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval

async def on_update_report(data, ven_id, resource_id, measurement):
    """
    Callback that receives report data from the VEN and handles it.
    """
    for time, value in data:
        print(f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")

async def event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    print(f"VEN {ven_id} responded to Event {event_id} with: {opt_type}")


# Create the server object with X.509 certificate and private key
server = OpenADRServer(vtn_id='BensVTN',
                       http_cert='vtn_cert.pem',
                       http_key='vtn_key.pem',
                       http_ca_file='ca.crt',
                       http_port=8080,
                       http_host='0.0.0.0',
                       http_path_prefix='/OpenADR2/Simple/2.0b',
                       requested_poll_freq=timedelta(seconds=10),
                       ven_lookup=ven_lookup)

# Add the handler for client (VEN) registrations
server.add_handler('on_create_party_registration', on_create_party_registration)

# Add the handler for report registrations from the VEN
server.add_handler('on_register_report', on_register_report)

# Add a prepared event for a VEN that will be picked up when it polls for new messages.
server.add_event(ven_id='ven_id_123',
                 signal_name='simple',
                 signal_type='level',
                 intervals=[{'dtstart': dtstart,
                             'duration': timedelta(minutes=10),
                             'signal_payload': 1}],
                 callback=event_response_callback)

# Run the server on the asyncio event loop
loop = asyncio.get_event_loop()
loop.create_task(server.run())
loop.run_forever()
