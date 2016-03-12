def get_dallas_temps():
    sensors = {
        'grow_bed': '28-02157162fdff',
        'fish_tank': '28-0115712f76ff',
        'sump_tank': '28-011562afe3ff',
    }

    sensor_dir = '/sys/bus/w1/devices/'
    sensor_end = '/w1_slave'

    tempDict = {}

    for key, value in sensors.iteritems():
        device_directory = sensor_dir + value + sensor_end
        f = open(device_directory, "r")
        lines = f.readlines()
        f.close()

        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
        tempDict[key] = temp_c

    return tempDict

if __name__ == '__main__':
    temp = get_dallas_temps()
    print temp
