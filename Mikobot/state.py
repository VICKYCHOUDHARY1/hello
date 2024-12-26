# Imports
from aiohttp import ClientSession
from httpx import AsyncClient, Timeout
from Python_ARQ import ARQ

# Constants
ARQ_API_KEY = "ERTMOF-BGEQGE-RGHHYB-LLZWYD-ARQ"  # GET API KEY FROM @ARQRobot
ARQ_API_URL = "https://arq.hamker.dev"

# Placeholder for global variables
session = None
state = None
arq = None


async def initialize_state():
    """
    Initialize async clients and ARQ connection.
    """
    global session, state, arq

    # Initialize aiohttp ClientSession
    session = ClientSession()

    # Initialize HTTPx AsyncClient
    state = AsyncClient(
        http2=True,
        verify=False,
        headers={
            "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
        },
        timeout=Timeout(20),
    )

    # Initialize ARQ with aiohttp ClientSession
    arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)


async def close_state():
    """
    Close async clients properly.
    """
    global session, state

    if session:
        await session.close()
    if state:
        await state.aclose()
