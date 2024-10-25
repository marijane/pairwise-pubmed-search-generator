import streamlit as st

pubmed_search_url = "https://pubmed.ncbi.nlm.nih.gov/?term="

st.set_page_config(page_title="Pairwise PubMed Search Generator")
st.title("Pairwise PubMed Search Generator")
st.write("This app generates PubMed search strings from two lists of terms. Use it to combine a list of MeSH Main Headings with a list of MeSH Subheadings, or to work around the truncation linitation in PubMed's proximity search.")

with st.form("enter_terms_form"):
    with st.expander("Pairwise Mesh Main Heading/Subheading Search"):

        mesh_terms = st.text_area("Enter MeSH Main Headings, one per line.", height=300 ,value="asthenia\nfatigue\nfrailty\nmuscle weakness\nmuscle atrophy").splitlines()
        majr = st.checkbox("MeSH Major Topic")
        subheadings = st.text_area("Enter MeSH Subheadings, one per line.", height=200, value="diagnosis\nepidemiology").splitlines()
        
        submitted_mesh = st.form_submit_button("Generate pairwise MeSH search string")
        
        if submitted_mesh:
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

    with st.expander("Pairwise Keyword Proximity Search"):
        proximity_field = st.selectbox("Proximity field", options=["ti", "tiab", "ad"], index=1)
        proximity_distance = st.text_input("Proximity distance", value="2")

        topic1_terms = st.text_area("Enter Topic 1 terms, one per line, no truncation.", 
                                    value="asthenia\nfatigue\nfrailty\nmuscle weakness\nmuscular weakness\nmuscle atrophy\nmuscular atrophy\ndebility\nsarcopenia", 
                                    height=300
                                    ).splitlines()
                                    
        topic2_terms = st.text_area("Enter Topic 2 terms, one per line, no truncation.", 
                                    value="assess\nassessment\ndiagnosis\ndiagnoses\ndiagnostic\nevaluate\nevaluation\ninstrument\ninstruments\nindex\nmeasure\nmeasures\nscreen\nscreens\nscreening\nscreenings\ntest\ntests\ntesting\ntool\ntools",
                                    height=500, 
                                    ).splitlines() 
        
        submitted_proximity = st.form_submit_button("Generate pairwise proximity search string")

        if submitted_proximity:

            keyword_proximity_searches = [
                f'"{topic1_term} {topic2_term}"[{proximity_field}:~{proximity_distance}]'
                for topic1_term in topic1_terms
                for topic2_term in topic2_terms
            ]

            keyword_proximity_search_string = " OR ".join(keyword_proximity_searches)


            st.write(keyword_proximity_search_string)

            st.link_button(label="Search PubMed with pairwise keyword proximity search string",
                        url=pubmed_search_url+keyword_proximity_search_string.replace(" ", "+"))
            
            if submitted_mesh:
                mesh_proximity_search_string = " OR ".join([mesh_search_string, keyword_proximity_search_string])

                st.link_button(label="Search PubMed with full MeSH/proximity search string", 
                            url=pubmed_search_url+mesh_proximity_search_string.replace(" ", "+"))

    with st.expander("Pairwise Keyword Intersection Search (Boolean AND)"):
        topic1_terms = st.text_area("Enter Topic 1 terms, one per line", 
                                    value="asthenia\nfatigue\nfrailty\nmusc* weak*\nmusc* atroph*\nmusc* atrophy\ndebilit*\nsarcopenia*", 
                                    height=300
                                    ).splitlines()
                                    
        topic2_terms = st.text_area("Enter Topic 2 terms, one per line", 
                                    value="assess*\ndiagnos*\nevaluat*\ninstrument*\nindex\nindices\nmeasure*\nscreen*\ntest*\ntool*",
                                    height=500, 
                                    ).splitlines() 
        
        submitted_intersection = st.form_submit_button("Generate pairwise intersection search string")

        if submitted_intersection:

            keyword_intersection_searches = [
                "(" + topic1_term + " AND " + topic2_term + ")"
                for topic1_term in topic1_terms
                for topic2_term in topic2_terms
            ]

            keyword_intersection_search_string = " OR ".join(keyword_intersection_searches)


            st.write(keyword_intersection_search_string)

            st.link_button(label="Search PubMed with pairwise keyword intersection search string",
                        url=pubmed_search_url+keyword_intersection_search_string.replace(" ", "+"))
            
            if submitted_mesh:
                mesh_intersection_search_string = " OR ".join([mesh_search_string, keyword_intersection_search_string])

                st.link_button(label="Search PubMed with full MeSH/intersection search string", 
                            url=pubmed_search_url+mesh_intersection_search_string.replace(" ", "+"))
