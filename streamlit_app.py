import streamlit as st

pubmed_search_url = "https://pubmed.ncbi.nlm.nih.gov/?term="
text_area_height = 250

st.set_page_config(page_title="Pairwise PubMed Search Generator", layout="wide", page_icon="🔎")
st.title("Pairwise PubMed Search Generator")
st.write("This app generates PubMed search strings from two lists of terms. Use it to combine a list of MeSH Main Headings with a list of MeSH Subheadings, or to work around the truncation linitation in PubMed's proximity search.")

with st.form("enter_terms_form"):
    st.header("Pairwise Mesh Main Heading/Subheading Search", divider=True)
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        mesh_terms = st.text_area("Enter MeSH Main Headings, one per line.", 
                                height=text_area_height ,
                                value="asthenia\nfatigue\nfrailty\nmuscle weakness\nmuscle atrophy").splitlines()
    with mcol2:
        subheadings = st.text_area("Enter MeSH Subheadings, one per line.", 
                                height=text_area_height, value="diagnosis\nepidemiology").splitlines()
    
    majr = st.checkbox("MeSH Major Topic")
    
    st.header("Pairwise Keyword Proximity Search", divider=True)
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        topic1_terms = st.text_area("Enter Topic 1 terms, one per line, no truncation.", 
                                    value="asthenia\nfatigue\nfrailty\nmuscle weakness\nmuscular weakness\nmuscle atrophy\nmuscular atrophy\ndebility\nsarcopenia", 
                                    height=text_area_height
                                    ).splitlines()
        proximity_field = st.selectbox("Proximity field", options=["ti", "tiab", "ad"], index=1)
    with pcol2:                                
        topic2_terms = st.text_area("Enter Topic 2 terms, one per line, no truncation.", 
                                    value="assess\nassessment\ndiagnosis\ndiagnoses\ndiagnostic\nevaluate\nevaluation\ninstrument\ninstruments\nindex\nmeasure\nmeasures\nscreen\nscreens\nscreening\nscreenings\ntest\ntests\ntesting\ntool\ntools",
                                    height=text_area_height, 
                                    ).splitlines() 
        proximity_distance = st.text_input("Proximity distance", value="2")

    st.header("Pairwise Keyword Intersection Search (Boolean AND)", divider=True)
    icol1, icol2 = st.columns(2)
    with icol1:
        topic1_terms = st.text_area("Enter Topic 1 terms, one per line", 
                                    value="asthenia\nfatigue\nfrailty\nmusc* weak*\nmusc* atroph*\nmusc* atrophy\ndebilit*\nsarcopenia*", 
                                    height=text_area_height
                                    ).splitlines()

    with icol2:                     
        topic2_terms = st.text_area("Enter Topic 2 terms, one per line", 
                                    value="assess*\ndiagnos*\nevaluat*\ninstrument*\nindex\nindices\nmeasure*\nscreen*\ntest*\ntool*",
                                    height=text_area_height
                                    ).splitlines() 
    submitted = st.form_submit_button("Generate pairwise search strings")

    if submitted:
        if majr:
            field = "[majr]"
        else:
            field = "[mh]"

        mesh_searches = [
            mesh_term + "/" + subheading + field
            for mesh_term in mesh_terms
            for subheading in subheadings
        ]
        mesh_search_string = " OR ".join(mesh_searches)
        st.write(mesh_search_string)
        st.link_button(label="Search PubMed with pairwise MeSH heading/subheading search string",
                    url=pubmed_search_url+mesh_search_string.replace(" ", "+"))

        keyword_proximity_searches = [
            f'"{topic1_term} {topic2_term}"[{proximity_field}:~{proximity_distance}]'
            for topic1_term in topic1_terms
            for topic2_term in topic2_terms
        ]
        keyword_proximity_search_string = " OR ".join(keyword_proximity_searches)
        st.write(keyword_proximity_search_string)
        st.link_button(label="Search PubMed with pairwise keyword proximity search string",
                    url=pubmed_search_url+keyword_proximity_search_string.replace(" ", "+"))
        
        mesh_proximity_search_string = " OR ".join([mesh_search_string, keyword_proximity_search_string])
        st.link_button(label="Search PubMed with pairwise MeSH/proximity search string",
                    url=pubmed_search_url+mesh_proximity_search_string.replace(" ", "+"))

        keyword_intersection_searches = [
            "(" + topic1_term + " AND " + topic2_term + ")"
            for topic1_term in topic1_terms
            for topic2_term in topic2_terms
        ]

        keyword_intersection_search_string = " OR ".join(keyword_intersection_searches)
        st.write(keyword_intersection_search_string)
        st.link_button(label="Search PubMed with pairwise keyword intersection search string",
                    url=pubmed_search_url+keyword_intersection_search_string.replace(" ", "+"))

        mesh_intersection_search_string = " OR ".join([mesh_search_string, keyword_intersection_search_string])
        st.link_button(label="Search PubMed with pairwise MeSH/intersection search string",
                    url=pubmed_search_url+mesh_intersection_search_string.replace(" ", "+"))
