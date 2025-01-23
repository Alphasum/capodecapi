from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import asyncio

# FastAPI app setup
app = FastAPI()

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define today's and tomorrow's dates
today = datetime.now()
tomorrow = today + timedelta(days=1)

# Sources to scrape
sources = [
    'https://typersi.com/typer/60049/omwami1',
    'https://typersi.com/typer/25381/pitwol',
    'https://typersi.com/typer/26351/gasior',
    'https://typersi.com/typer/45156/Vilenma',
    'https://typersi.com/typer/26896/Wilenma',
    'https://typersi.com/typer/61475/NAIROBI',
    'https://typersi.com/typer/46504/CLIMAX',
    'https://typersi.com/typer/45765/AWTOOLS',
    'https://typersi.com/typer/31024/wp76',
    'https://typersi.com/typer/54483/Cobra2407',
    'https://typersi.com/typer/61037/Dzaro',
    'https://typersi.com/typer/60183/michuulol',
    'https://typersi.com/typer/24977/przemas04',
    'https://typersi.com/typer/31864/Kowalsky',
    'https://typersi.com/typer/60357/White100k',
    'https://typersi.com/typer/32078/monkey19', 
    'https://typersi.com/typer/58381/Lion77', 
    'https://typersi.com/typer/61621/Koiborirei'
]

# Function to scrape data
def fetch_data():
    data = []
    for url in sources:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract effectiveness
        effectiveness_div = soup.find('div', class_='progressC')
        effectiveness = effectiveness_div.find('span', class_='d-inline').text if effectiveness_div else '0'

        # Extract table rows
        table = soup.find('table', class_='table bg-theme align-middle text-nowrap')
        if table:
            rows = table.find('tbody').find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    day = cols[1].text.strip()
                    time = cols[2].text.strip()
                    match_league = cols[3].text.strip()
                    tip = cols[4].text.strip()
                    odd = cols[6].text.strip()
                    score = cols[8].text.strip()

                    # Check if day is today or tomorrow
                    if day in [today.strftime('%d'), tomorrow.strftime('%d')]:
                        data.append({
                            'Day': day,
                            'Time': time,
                            'Match/League': match_league,
                            'Tip': tip,
                            'Odd': odd,
                            'Score': score,
                            'Effectiveness': effectiveness
                        })
    return sorted(data, key=lambda x: int(x['Effectiveness']), reverse=True)

# HTTP route for fetching data
@app.get("/data")
async def get_data():
    data = fetch_data()
    return {"data": data}

# WebSocket route to stream table data
@app.websocket("/data/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = fetch_data()
        await websocket.send_json(data)
        await asyncio.sleep(3600)  # Refresh data every 1 hour
