# Copy-pasted with some modifications from 
# https://en.wikipedia.org/wiki/Sunrise_equation#Example_of_implementation_in_Python

import logging
from datetime import datetime, tzinfo
from math import acos, asin, ceil, cos, degrees, fmod, radians, sin, sqrt
import re

log = logging.getLogger()


def _ts2human(ts: int | float, debugtz: tzinfo | None) -> str:
    return str(datetime.fromtimestamp(ts, debugtz))


def j2ts(j: float | int) -> float:
    return (j - 2440587.5) * 86400


def ts2j(ts: float | int) -> float:
    return ts / 86400.0 + 2440587.5


def _j2human(j: float | int, debugtz: tzinfo | None) -> str:
    ts = j2ts(j)
    return f'{ts} = {_ts2human(ts, debugtz)}'


def _deg2human(deg: float | int) -> str:
    """Transform geographical coordinate in decimal degrees into sexagesimal human-readable
    format (degree, arcminute and arcsecond).

    Args:
        deg (float | int): Geographical coordinate in decimal degrees.

    Returns:
        str: Sexagesimal coordinate.
    """    
    x = int(deg * 3600.0)
    num = f'∠{deg:.3f}°'
    rad = f'∠{radians(deg):.3f}rad'
    human = f'∠{x // 3600}°{x // 60 % 60}′{x % 60}″'
    return f'{rad} = {human} = {num}'

def _parse_coord_str(coord_str: str) -> float:
    """Convert string representing sexagesimal lattitude or longitude into decimal degrees.

    Args:
        coord_str (str): String representing sexagesimal lattitude or longitude.

    Returns:
        float: Coordinate value.
    """    
    deg = 0
    for i, str_ in enumerate(re.split("°|′|″", coord_str)):
        if str_.isdigit():
            deg += int(str_) / 60 ** i
        elif str_ in "SW":
            deg *= -1
    return deg

def human2deg(human: str) -> tuple[float, float]:
    """Transform geographical coordinate in sexagesimal human-readable
    format (degree, arcminute and arcsecond) into decimal degrees.

    Args:
        human (str): Geographical coordinate in sexagesimal format.

    Returns:
        tuple[float, float]: Geographical coordinate in decimal degrees.
    """   
    lat, long = map(_parse_coord_str, human.split(" "))
    return lat, long


def calc(
        current_timestamp: float,
        lat: float,
        long: float,
        elevation: float = 0.0,
        *,
        debugtz: tzinfo | None = None,
    ) -> tuple[float, float, float, float] | tuple[None, None, None, bool]:
    """Calculate the sunrise, sunset time (timestamp) and the day length (in seconds) for a given
      date.

    Args:
        current_timestamp (float): Current time in seconds since the Epoch.
        lat (float): Latitude in decimal degrees.
        long (float): Longitude in decimal degrees.
        elevation (float, optional): Elevation of the observer in meters. Defaults to 0.0.
        debugtz (tzinfo | None, optional): Label of the timezone. Defaults to None.

    Returns:
        tuple[float, float, float, float] | tuple[None, None, None, bool]: Tuple containing POSIX
          timestamps of the sunrize and sunset, the day length in seconds.
    """    
    log.debug(f'Latitude               f       = {_deg2human(lat)}')
    log.debug(f'Longitude              l_w     = {_deg2human(long)}')
    log.debug(f'Now                    ts      = {_ts2human(current_timestamp, debugtz)}')

    J_date = ts2j(current_timestamp)
    log.debug(f'Julian date            j_date  = {J_date:.3f} days')

    # Julian day
    # TODO: ceil ?
    n = ceil(J_date - (2451545.0 + 0.0009) + 69.184 / 86400.0)
    log.debug(f'Julian day             n       = {n:.3f} days')

    # Mean solar time
    J_ = n + 0.0009 - long / 360.0
    log.debug(f'Mean solar time        J_      = {J_:.9f} days')

    # Solar mean anomaly
    # M_degrees = 357.5291 + 0.98560028 * J_  # Same, but looks ugly
    M_degrees = fmod(357.5291 + 0.98560028 * J_, 360)
    M_radians = radians(M_degrees)
    log.debug(f'Solar mean anomaly     M       = {_deg2human(M_degrees)}')

    # Equation of the center
    C_degrees = 1.9148 * sin(M_radians) + 0.02 * sin(2 * M_radians) + 0.0003 * sin(3 * M_radians)
    # The difference for final program result is few milliseconds
    # https://www.astrouw.edu.pl/~jskowron/pracownia/praca/sunspot_answerbook_expl/expl-4.html
    # e = 0.01671
    # C_degrees = \
    #     degrees(2 * e - (1 / 4) * e ** 3 + (5 / 96) * e ** 5) * sin(M_radians) \
    #     + degrees(5 / 4 * e ** 2 - (11 / 24) * e ** 4 + (17 / 192) * e ** 6) * sin(2 * M_radians) \
    #     + degrees(13 / 12 * e ** 3 - (43 / 64) * e ** 5) * sin(3 * M_radians) \
    #     + degrees((103 / 96) * e ** 4 - (451 / 480) * e ** 6) * sin(4 * M_radians) \
    #     + degrees((1097 / 960) * e ** 5) * sin(5 * M_radians) \
    #     + degrees((1223 / 960) * e ** 6) * sin(6 * M_radians)

    log.debug(f'Equation of the center C       = {_deg2human(C_degrees)}')

    # Ecliptic longitude
    # L_degrees = M_degrees + C_degrees + 180.0 + 102.9372  # Same, but looks ugly
    L_degrees = fmod(M_degrees + C_degrees + 180.0 + 102.9372, 360)
    log.debug(f'Ecliptic longitude     L       = {_deg2human(L_degrees)}')

    Lambda_radians = radians(L_degrees)

    # Solar transit (julian date)
    J_transit = 2451545.0 + J_ + 0.0053 * sin(M_radians) - 0.0069 * sin(2 * Lambda_radians)
    log.debug(f'Solar transit time     J_trans = {_j2human(J_transit, debugtz)}')

    # Declination of the Sun
    sin_d = sin(Lambda_radians) * sin(radians(23.4397))
    # cos_d = sqrt(1-sin_d**2) # exactly the same precision, but 1.5 times slower
    cos_d = cos(asin(sin_d))

    # Hour angle
    some_cos = (sin(radians(-0.833 - 2.076 * sqrt(elevation) / 60.0)) - sin(radians(lat)) * sin_d) / (cos(radians(lat)) * cos_d)
    try:
        w0_radians = acos(some_cos)
    except ValueError:
        return None, None, None, some_cos > 0.0
    w0_degrees = degrees(w0_radians)  # 0...180
    day_length = w0_degrees / (180 / (24 * 3600)) # in seconds

    log.debug(f'Hour angle             w0      = {_deg2human(w0_degrees)}')

    j_rise = J_transit - w0_degrees / 360
    j_set = J_transit + w0_degrees / 360

    log.debug(f'Sunrise                j_rise  = {_j2human(j_rise, debugtz)}')
    log.debug(f'Sunset                 j_set   = {_j2human(j_set, debugtz)}')
    log.debug(f'Day length                       {day_length / 3600:.3f} hours')

    return j2ts(j_rise), j2ts(j_set), j2ts(J_transit), day_length