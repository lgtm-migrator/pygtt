import aiohttp
from .consts import BASE_URL
from .models import Stop, Bus
import async_timeout
from bs4 import BeautifulSoup


class PyGTT():

    def __init__(
        self,
        stop_name: str,
        session: aiohttp.ClientSession = None,
        request_timeout: int = 8,
    ) -> "PyGTT":
        self._stop = Stop(stop_name, None)
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


    async def _parse_data(self, data):
        """Parse the data from PyGTT."""
        with BeautifulSoup(r.text, 'html.parser') as soup:
            time_table = soup.findAll('table')[0]

            for row in main_table.findAll('tr'): # Get the rows in the time table.
                # Every row represents a bus at the stop.
                for column in row.findAll('td'):
                    time = {}
                    if column.findAll('a'):
                        bus.name = column.find('a').text
                    else:
                        if column.text:
                            run = column.text
                            if '*' not in column.text:
                                time['isRealtime'] = 'false'
                            else:
                                time['isRealtime'] = 'true'
                                run = column.text.replace('*', '')
                            time['run'] = run
                            bus['time'].append(time)
                bus_list.append(bus)
            return bus_list

    async def get_state(self):
        """Get the state of the stop."""
        await self._request()
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