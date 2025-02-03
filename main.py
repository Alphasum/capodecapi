import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def fetch_data(urls):
    """Fetch and parse data from the given URLs."""
    all_data = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure the request was successful
            soup = BeautifulSoup(response.text, 'html.parser')

            # Locate the effectiveness in the HTML
            effectiveness_section = soup.find('div', class_='progressC')
            effectiveness = effectiveness_section.find('span', class_='d-inline').text.strip() if effectiveness_section else '0'

            # Locate the table in the HTML
            table = soup.find('table', {'class': 'table bg-theme align-middle text-nowrap'})
            rows = table.find('tbody').find_all('tr')

            for row in rows:
                cols = row.find_all('td')
                if cols:
                    day = cols[1].text.strip()
                    time = cols[2].text.strip()
                    match_league = cols[4].text.strip()
                    tip = cols[5].text.strip()
                    odd = cols[7].text.strip()

                    # Extract score and outcome
                    score_cell = cols[8]
                    if score_cell.find('div'):
                        score = score_cell.find('div').text.strip()
                        outcome = 'Win' if '_twin' in score_cell['class'] else 'Loss'
                    else:
                        score = score_cell.text.strip()
                        outcome = 'N/A'

                    all_data.append([day, time, match_league, tip, odd, score, outcome, effectiveness])
        except Exception as e:
            st.error(f"An error occurred while fetching data from {url}: {e}")

    return all_data

def main():
    st.title("Web Scraper for Sports Predictions")

    # List of source URLs
    urls = [
        'https://typersi.com/typer/24683/tagog',
        'https://typersi.com/typer/52132/kasa',
        'https://typersi.com/typer/25052/Machin1990',
        'https://typersi.com/typer/61947/SweetLu2',
        'https://typersi.com/typer/24671/Bonifazius',
        'https://typersi.com/typer/50752/Kolba1',
        'https://typersi.com/typer/27314/czorny',
        'https://typersi.com/typer/36324/Skubi19',
        'https://typersi.com/typer/31009/rodeoboy',
        'https://typersi.com/typer/25015/Rubinstein',
        'https://typersi.com/typer/50750/Mikla84',
        'https://typersi.com/typer/47042/lech7321',
        'https://typersi.com/typer/24893/jemni78', 
        'https://typersi.com/typer/26101/nikholas',
        'https://typersi.com/typer/24820/handball',
        'https://typersi.com/typer/41811/piekny',
        'https://typersi.com/typer/24999/Ruch1920',
        'https://typersi.com/typer/60283/DR15',
        'https://typersi.com/typer/61268/ERGASHEV',
        'https://typersi.com/typer/25432/gregory198',
        'https://typersi.com/typer/25283/VersaceNo1',
        'https://typersi.com/typer/61583/Styleking',
        'https://typersi.com/typer/61054/Bart87',
        'https://typersi.com/typer/50367/ProTypy',
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
        'https://typersi.com/typer/61621/Koiborirei',
        'https://typersi.com/typer/39910/RiczardGir',
        'https://typersi.com/typer/52038/ramzes',
        'https://typersi.com/typer/39877/Cactus',
        'https://typersi.com/typer/26895/Kuckisan',
        'https://typersi.com/typer/60913/Rem999',
        'https://typersi.com/typer/37042/Lenkapas',
        'https://typersi.com/typer/58740/Ciechan',
        'https://typersi.com/typer/51290/Santi07',
        'https://typersi.com/typer/44326/Lorinus',
        'https://typersi.com/typer/51543/rav303',
        'https://typersi.com/typer/61472/NikhilSB',
        'https://typersi.com/typer/51361/DODONI',
        'https://typersi.com/typer/50239/Rekin1981',
        'https://typersi.com/typer/25283/VersaceNo1',
        'https://typersi.com/typer/59333/banguch',
        'https://typersi.com/typer/58197/LUKI23',
        'https://typersi.com/typer/52454/Kaka',
        'https://typersi.com/typer/48312/RandyKings',
        'https://typersi.com/typer/48000/BAYERN777',
        'https://typersi.com/typer/24813/kapsel007',
        'https://typersi.com/typer/61099/Kaczor',
        'https://typersi.com/typer/61158/realproper',
        'https://typersi.com/typer/59310/VitOld',
        'https://typersi.com/typer/36030/BLX',
        'https://typersi.com/typer/24695/Maczan88'
    ]

    st.write("Fetching data from multiple sources...")

    # Fetch data
    data = fetch_data(urls)

    if data:
        # Create a DataFrame
        columns = [
            "Day", "Time", "Match/League", "Tip", "Odds", "Score", "Outcome", "Effectiveness"
        ]
        df = pd.DataFrame(data, columns=columns)

        # Filter data for today's and tomorrow's dates
        today = datetime.now().day
        tomorrow = (datetime.now() + timedelta(days=1)).day
        df = df[df["Day"].astype(int).isin([today, tomorrow])]

        # Convert effectiveness to numeric for sorting
        df["Effectiveness"] = pd.to_numeric(df["Effectiveness"], errors='coerce')
        df = df.sort_values(by="Effectiveness", ascending=False)

        # Display the table
        st.write("### Extracted and Filtered Table")
        st.dataframe(df)

        # Option to download the table as CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="sports_predictions_filtered.csv",
            mime="text/csv",
        )

        # Option to download the table as JSON
        json_data = df.to_json(orient="records")
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="sports_predictions_filtered.json",
            mime="application/json",
        )
    else:
        st.write("No data available or failed to fetch data.")

if __name__ == "__main__":
    main()
