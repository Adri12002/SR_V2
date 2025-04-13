import streamlit as st
import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_data():
    data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.cybermalveillance.gouv.fr/tous-les-contenus/annuaire-des-prestataires/liste")
        page.wait_for_selector("table.dataTable")

        while True:
            rows = page.query_selector_all("table.dataTable tbody tr")
            for row in rows:
                cols = row.query_selector_all("td")
                if len(cols) >= 4:
                    data.append({
                        "Raison Sociale": cols[0].inner_text().strip(),
                        "Site Web": cols[1].inner_text().strip(),
                        "Ville": cols[2].inner_text().strip(),
                        "Domaine": cols[3].inner_text().strip()
                    })

            next_btn = page.query_selector("a#DataTables_Table_0_next")
            if "disabled" in next_btn.get_attribute("class"):
                break
            next_btn.click()
            page.wait_for_timeout(1500)

        browser.close()
    return pd.DataFrame(data)

def save_to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

st.title("Scraper des prestataires de cybersécurité")

if st.button("Lancer le scraping"):
    with st.spinner("Scraping en cours..."):
        df = scrape_data()
        st.success("Scraping terminé !")
        st.dataframe(df)

        output = save_to_excel(df)
        st.download_button(
            label="📥 Télécharger Excel",
            data=output,
            file_name="prestataires_cybermalveillance.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )