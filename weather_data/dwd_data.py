import time

from deutschland import dwd
from deutschland.dwd.api import default_api
from deutschland.dwd.model.station_overview import StationOverview
from deutschland.dwd.model.error import Error
from deutschland.dwd.model.station_overview_extended_get_station_ids_parameter_inner \
    import StationOverviewExtendedGetStationIdsParameterInner
from pprint import pprint


# Defining the host is optional and defaults to https://app-prod-ws.warnwetter.de/v30
# See configuration.py for a list of all supported configuration parameters.
configuration = dwd.Configuration(
    host = "https://app-prod-ws.warnwetter.de/v30"
)


# Enter a context with an instance of the API client.
with dwd.ApiClient() as api_client:
    # Create an instance of the API class.
    api_instance = default_api.DefaultApi(api_client)

    # The stations_ids parameter uses the StationOverviewExtendedGetStationIdsParameterInner
    # class and the DWD weather station identifier that can be found in the list on:
    # https://www.dwd.de/DE/leistungen/klimadatendeutschland/stationsliste.html
    station_ids = [
        StationOverviewExtendedGetStationIdsParameterInner(station_ids="H174"),
    ]

    # Line 892 of the api_client.py needed to be modified to:
    # >>> param_value_full = (base_name, [d[param_name] for d in param_value])
    # Without the modification the response is empty.
    try:
        # Response contains weather station data.
        api_response = api_instance.station_overview_extended_get(station_ids=station_ids)
        pprint(api_response)
    except dwd.ApiException as e:
        print("Exception when calling DefaultApi->station_overview_extended_get: %s\n" % e)
