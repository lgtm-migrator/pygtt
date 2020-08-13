import aiohttp
from .consts import BASE_URL
from .models import Stop, Bus, BusTime
import async_timeout
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class PyGTT():

    def __init__(
        self,
        stop_name: str,
        session: aiohttp.ClientSession = None,
        request_timeout: int = 8,
    ) -> "PyGTT":
        self._stop = Stop(stop_name)
        self._session = session
        self._close_session = False
        self._request_timeout = request_timeout

    async def _request(self) -> None:
        """Handle the request to PyGTT."""

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self._request_timeout):
                response = await self._session.request(
                    "GET",
                    BASE_URL.format(self._stop.name),
                )
                response.raise_for_status()
        except Exception: # TODO: Handle exceptions
            raise Exception()

        return (await response.text())


    def _parse_data(self, data):
        """Parse the data from PyGTT."""
        soup = BeautifulSoup(data, 'html.parser')
        time_table = soup.findAll('table')[0]
        self._stop.bus_list = []
        for row in time_table.findAll('tr'): # Get the rows in the time table.
            # Every row represents a bus at the stop.
            bus = None
            for column in row.findAll('td'):
                if column.findAll('a'):
                    bus = Bus(column.find('a').text)
                else:
                    time_str = column.text
                    time = datetime.strptime(
                        time_str.replace("*", ""), 
                        "%H:%M"
                    )
                    time = time.replace(
                        year = datetime.now().year,
                        month = datetime.now().month,
                        day = datetime.now().day,
                    )
                    if time <= datetime.now():
                        time = time + timedelta(days=1)
                    bus.time.append(
                        BusTime(
                            time,
                            "*" in time_str
                        )
                    )
            self._stop.bus_list.append(bus)
        return self._stop

    async def get_state(self):
        """Get the state of the stop."""
        self._stop = self._parse_data(await self._request())
        return self._stop

    async def close(self) -> None:
        """Close the session."""
        if self._close_session and self._session:
            await self._session.close()

    async def __aenter__(self) -> "PyGTT":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()