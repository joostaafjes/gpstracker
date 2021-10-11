import datetime

from .models import GpsTrackerMessage

bat_levels = [
    {'low': 4.00, 'high': 4.028, 'p_low': 80, 'p_high': 100},
    {'low': 3.85, 'high': 4.00, 'p_low': 60, 'p_high': 80},
    {'low': 3.70, 'high': 3.85, 'p_low': 40, 'p_high': 60},
    {'low': 3.40, 'high': 3.70, 'p_low': 20, 'p_high': 40},
    {'low': 3.10, 'high': 3.40, 'p_low': 0, 'p_high': 20}
]

class GpsTracker():
    def __init__(self, bn, payload, bt, message):
        gpstracker_msg = GpsTrackerMessage(deveui=bn)
        pass

    @staticmethod
    def create(data, message):
        if 'payload' in data:
            deveui = data['bn']
            bt = data['bt']
            date = datetime.datetime.fromtimestamp(bt)
            payload = data['payload']
            print(f'date: {date}')

            latitude = payload[0:8]
            latitude = int(latitude, 16) / 1000000
            print(f'latitude: {latitude}')

            longitude = payload[8:16]
            longitude = int(longitude, 16) / 1000000
            print(f'longitude: {longitude}')

            alarm = payload[16:18]
            print(f'alarm: {alarm}')
            alarm = int(alarm, 16)
            alarm = (alarm & 0x40) >> 6
            print(f'alarm: {alarm}')

            bat = payload[16:20]
            bat = int(bat, 16)
            bat = (bat & 0x3FFF) / 1000
            bat_per = GpsTracker.bat_percentage(bat)
            print(f'bat: {bat} ({bat_per} %)')

            flag = payload[20:22]
            flag = int(flag, 16)
            md = flag >> 6
            lon = (flag >> 5) & 1
            firmware_version = flag & 0x1f
            print(f'md: {md}')
            print(f'lon: {lon}')
            print(f'firmware version: {firmware_version}')

            roll = None
            pitch = None
            hdop = None
            altitude = None

            if len(payload) > 22:
                print(f'longer payload: {payload[22:]}')
                roll = payload[22:26]
                roll = int(roll, 16)
                if (roll & 0x8000) == 0:
                    roll /= 100
                    print(f'roll: {roll} degree')
                else:
                    print(f'roll error: {roll}')

                pitch = payload[26:30]
                pitch = int(pitch, 16)
                if (pitch & 0x8000) == 0:
                    pitch = (pitch - 0x10000) / 100
                else:
                    print(f'pitch error: {pitch}')

                hdop = payload[30:32]
                hdop = int(hdop, 16)
                if hdop > 0:
                    hdop /= 100
                    print(f'hdop: {hdop}')

                altitude = payload[32:36]
                altitude = int(altitude, 16) / 100
                print(f'altitude: {altitude} meter')
            gpstracker = GpsTrackerMessage(deveui=deveui,
                                           date=date,
                                           payload=payload,
                                           latitude=latitude,
                                           longitude=longitude,
                                           alarm=alarm,
                                           battery=bat,
                                           battery_perc=bat_per,
                                           led_activity=lon,
                                           movement_detection=md,
                                           roll=roll,
                                           pitch=pitch,
                                           altitude=altitude,
                                           hdop=hdop,
                                           message=message)
            gpstracker.save()
            return True
        return False

    @staticmethod
    def bat_percentage(bat):
        perc = None
        for level in bat_levels:
            if bat > level['low'] and bat <= level['high']:
                perc = level['p_low'] + (bat - level['low']) / (level['high'] - level['low']) * (level['p_high'] - level['p_low'])
        if bat > bat_levels[0]['high']:
            perc = bat_levels[0]['p_high']
        if bat < bat_levels[-1]['low']:
            perc = bat_levels[-1]['p_low']
        return int(perc)
