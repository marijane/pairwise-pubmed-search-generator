import streamlit as st

pubmed_search_url = "https://pubmed.ncbi.nlm.nih.gov/?term="
text_area_height = 250

mesh_term_example = "asthenia\nfatigue\nfrailty\nmuscle weakness\nmuscle atrophy"
subheading_example = "diagnosis\nepidemiology"
proximity_topic1_example = "asthenia\nfatigue\nfrailty\nmuscle weakness\nmuscular weakness\nmuscle atrophy\nmuscular atrophy\ndebility\nsarcopenia"
proximity_topic2_example = "assess\nassessment\ndiagnosis\ndiagnoses\ndiagnostic\nevaluate\nevaluation\ninstrument\ninstruments\nindex\nmeasure\nmeasures\nscreen\nscreens\nscreening\nscreenings\ntest\ntests\ntesting\ntool\ntools"
intersection_topic1_example = "asthenia\nfatigue\nfrailty\nmusc* weak*\nmusc* atroph*\nmusc* atrophy\ndebilit*\nsarcopenia*"
intersection_topic2_example = "assess*\ndiagnos*\nevaluat*\ninstrument*\nindex\nindices\nmeasure*\nscreen*\ntest*\ntool*"

def clear_form():
    st.session_state["mesh"] = ""
    st.session_state["subheadings"] = ""
    st.session_state["proximity topic 1"] = ""
    st.session_state["proximity topic 2"] = ""
    st.session_state["intersection topic 1"] = ""
    st.session_state["intersection topic 2"] = ""

def load_examples():
    st.session_state['mesh'] = mesh_term_example
    st.session_state['subheadings'] = subheading_example
    st.session_state["proximity topic 1"] = proximity_topic1_example
    st.session_state["proximity topic 2"] = proximity_topic2_example
    st.session_state["intersection topic 1"] = intersection_topic1_example
    st.session_state["intersection topic 2"] = intersection_topic2_example

st.set_page_config(page_title="Pairwise PubMed Search Generator", page_icon="🔎")
st.title("Pairwise PubMed Search Generator", anchor=False)
st.write("This app generates PubMed search strings from two lists of terms. Use it to combine a list of MeSH Main Headings with a list of MeSH Subheadings, or to work around the truncation linitation in PubMed's proximity search.")

with st.form("enter_terms_form", enter_to_submit=False):
    st.header("Pairwise Mesh Main/Subheading Search", divider=True, anchor=False)
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        mesh_terms = st.text_area(
            label       = "MeSH Main Headings, one per line.", 
            placeholder = mesh_term_example,
            height      = text_area_height,
            key         = "mesh",
        ).splitlines()

        subcol1, subcol2 = st.columns(2)
        with subcol1:
            majr = st.checkbox("MeSH Major Topic")
        with subcol2:
            noexp = st.checkbox("Do not explode")

    with mcol2:
        subheadings = st.text_area(
            label       = "Enter MeSH Subheadings, one per line.", 
            placeholder = subheading_example,
            height      = text_area_height, 
            key         = "subheadings"
        ).splitlines()
    
    st.header("Pairwise Keyword Proximity Search", divider=True, anchor=False)
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        proximity_topic1_terms = st.text_area(
            label       = "Enter Topic 1 terms, one per line, no truncation.", 
            placeholder = proximity_topic1_example, 
            height      = text_area_height,
            key         = "proximity topic 1",
        ).splitlines()
        proximity_field = st.selectbox("Proximity field", options=["ti", "tiab", "ad"], index=1)
    with pcol2:                                
        proximity_topic2_terms = st.text_area(
            label       = "Enter Topic 2 terms, one per line, no truncation.", 
            placeholder = proximity_topic2_example,
            height      = text_area_height, 
            key         = "proximity topic 2",
        ).splitlines()
        proximity_distance = st.number_input("Proximity distance", value=2)

    st.header("Pairwise Keyword Intersection Search (Boolean AND)", divider=True, anchor=False)
    icol1, icol2 = st.columns(2)
    with icol1:
        intersection_topic1_terms = st.text_area(
            label       = "Enter Topic 1 terms, one per line.", 
            placeholder = intersection_topic1_example,
            height      = text_area_height,
            key         = "intersection topic 1",
        ).splitlines()

    with icol2:                     
        intersection_topic2_terms = st.text_area(
            label       = "Enter Topic 2 terms, one per line.", 
            placeholder = intersection_topic2_example,
            height      = text_area_height,
            key         = "intersection topic 2"
        ).splitlines() 
    
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        load_example = st.form_submit_button(
            label = "Load example search terms",
            on_click = load_examples,
            use_container_width = True,
        )
    with bcol2:
        clear = st.form_submit_button(
            label   = "Clear form inputs",
            on_click = clear_form,
            use_container_width = True,
        )

    submitted = st.form_submit_button(
        label   = "Generate pairwise search strings and PubMed search buttons",
        use_container_width = True,
    )

    if submitted:
        if majr:
            field = "majr"
        else:
            field = "mh"
        if noexp:
            field = field + ":noexp"
        mesh_searches = [
            mesh_term + "/" + subheading + "[" + field + "]"
            for mesh_term in mesh_terms
            for subheading in subheadings
        ]
        mesh_search_string = " OR ".join(mesh_searches)
        if mesh_search_string: 
            with st.expander("Pairwise MeSH Main/Subheading Search String", expanded=True):
                st.write(mesh_search_string)
            st.link_button(
                label   = "Search PubMed with pairwise MeSH heading/subheading search string",
                url     = pubmed_search_url+mesh_search_string.replace(" ", "+"),
                type    = "primary",
            )

        keyword_proximity_searches = [
            f'"{ptopic1_term} {ptopic2_term}"[{proximity_field}:~{proximity_distance}]'
            for ptopic1_term in proximity_topic1_terms
            for ptopic2_term in proximity_topic2_terms
        ]
        keyword_proximity_search_string = " OR ".join(keyword_proximity_searches)
        if keyword_proximity_search_string:
            with st.expander("Pairwise Keyword Proximity Search String"):
                st.write(keyword_proximity_search_string)

            st.link_button(
                label   = "Search PubMed with pairwise keyword proximity search string",
                url     = pubmed_search_url+keyword_proximity_search_string.replace(" ", "+"),
                type    = "primary",
            )
            
            if mesh_search_string:
                mesh_proximity_search_string = " OR ".join([mesh_search_string, keyword_proximity_search_string])
                st.link_button(
                    label   = "Search PubMed with combined pairwise MeSH/proximity search strings",
                    url     = pubmed_search_url+mesh_proximity_search_string.replace(" ", "+"),
                    type    = "primary",
                )

        keyword_intersection_searches = [
            "(" + itopic1_term + " AND " + itopic2_term + ")"
            for itopic1_term in intersection_topic1_terms
            for itopic2_term in intersection_topic2_terms
        ]
        keyword_intersection_search_string = " OR ".join(keyword_intersection_searches)
        if keyword_intersection_search_string:
            with st.expander("Pairwise Keyword Intersection Search String"):
                st.write(keyword_intersection_search_string)
        
            st.link_button(
                label   = "Search PubMed with pairwise keyword intersection search string",
                url     = pubmed_search_url+keyword_intersection_search_string.replace(" ", "+"),
                type    = "primary",
            )

            mesh_intersection_search_string = " OR ".join([mesh_search_string, keyword_intersection_search_string])
            st.link_button(
                label   = "Search PubMed with combined pairwise MeSH/intersection search strings",
                url     = pubmed_search_url+mesh_intersection_search_string.replace(" ", "+"),
                type = "primary",
            )
