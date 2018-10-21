import json
from datetime import datetime
from bson.objectid import ObjectId


class SatelliteSet(dict):
    def __getattr__(self, name):
        return self[name]
    def __setattr__(self, name, value):
        self[name] = value
    def __str__(self, name, value):
        return str(dict(self))
    def __dict__(self):
        return dict(self)


def make_satellite_sets(output):
    results = []
    if isinstance(output, list):
        for item in output:
            satid = item.get('satellite_id')
            tstamp = dateify(item.get('timestamp'))

            for col in item.get('collection', []):

                s = SatelliteSet()

                s.satellite_id = satid
                s.timestamp = tstamp
                s.set_id = col.get('set_id')
                s.condition = col.get('condition')
                s.status = col.get('status')
                s.errors = '|'.join(col.get('errors', []))

                results.append(s)
    elif isinstance(output, dict):
        satid = output.get('satellite_id')
        tstamp = dateify(output.get('timestamp'))

        for col in output.get('collection', []):

            s = SatelliteSet()

            s.satellite_id = satid
            s.timestamp = tstamp
            s.set_id = col.get('set_id')
            s.condition = col.get('condition')
            s.status = col.get('status')
            s.errors = '|'.join(col.get('errors', []))

            results.append(s)
    return results

                
        



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return o.strftime("ISODate('%Y-%m-%dT%H:%M:%S')")
        return json.JSONEncoder.default(self, o)


def dateify(timestamp):
    if isinstance(timestamp, (float, int)):
        timestamp = datetime.utcfromtimestamp(timestamp)
    elif isinstance(timestamp, datetime): pass
    else: timestamp = datetime.utcnow()
    return timestamp.strftime('%Y-%m-%dT%H:%M:%S')


