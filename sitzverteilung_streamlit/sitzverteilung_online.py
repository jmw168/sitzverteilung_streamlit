import pandas as pd
import streamlit as st
from sitzverteilung.rechner.sainte_lague import SainteLague

DISTRIBUTION_METHODS = {
    "Sainte-Laguë Divisor": SainteLague("divisor"),
    "Sainte-Laguë ranking": SainteLague("rangzahl"),
}


def main():
    with st.form("number_of_rows"):
        number_of_rows = st.number_input("Number of parties:",
                                         value=5)
        st.form_submit_button()

    with st.form("votes"):
        methode = st.selectbox("Method", DISTRIBUTION_METHODS)
        seats = st.number_input("Number of seats:", value=15)
        votes_dict = {f"party{row_number + 1}": st.number_input(f"party {row_number + 1}", value=0, min_value=0) for
                      row_number in
                      range(number_of_rows)}
        form_button = st.form_submit_button()
        if form_button and sum(votes_dict.values()) == 0:
            st.error("You need more than 0 votes!")

    votes_frame = pd.DataFrame(data={'Stimmen': votes_dict.values()}, index=votes_dict.keys())
    if not sum(votes_dict.values()) == 0:
        seats_frame, lot = DISTRIBUTION_METHODS.get(methode)(votes_frame, seats)
        st.table(seats_frame)
        if lot:
            lot_parties = ', '.join([party for party in lot]).replace(',', ' and', len(lot))
            free_seats = seats - seats_frame['Sitze'].sum()
            st.warning(
                f"only {seats_frame['Sitze'].sum()} seats_frame allocated! \n\r "
                f"lottery for {free_seats} seat{'s' if not free_seats == 1 else ''} necessary between {lot_parties}")


if __name__ == '__main__':
    main()
