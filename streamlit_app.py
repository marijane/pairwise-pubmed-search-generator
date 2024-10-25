import streamlit as st

pubmed_search_url = "https://pubmed.ncbi.nlm.nih.gov/?term="
text_area_height = 250

mesh_term_example = \
"""
asthenia
fatigue
frailty
muscle weakness
muscle atrophy
"""
subheading_example = \
"""
diagnosis
epidemiology
"""
proximity_topic1_example = \
"""
asthenia
fatigue
frailty
muscle weakness
muscular weakness
muscle atrophy
muscular atrophy
debility
sarcopenia
"""
proximity_topic2_example = \
"""
assess
assessment
diagnosis
diagnoses
diagnostic
evaluate
evaluation
instrument
instruments
index
measure
measures
screen
screens
screening
screenings
test
tests
testing
tool
tools
"""
intersection_topic1_example = \
"""
asthenia
fatigue
frailty
musc* weak*
musc* atroph*
musc* atrophy
debilit*
sarcopenia*
"""
intersection_topic2_example = \
"""
assess*
diagnos*
evaluat*
instrument*
index
indices
measure*
screen*
test*
tool*
"""

def clear_form():
    st.session_state["mesh"] = ""
    st.session_state["subheadings"] = ""
    st.session_state["proximity topic 1"] = ""
    st.session_state["proximity topic 2"] = ""
    st.session_state["intersection topic 1"] = ""
    st.session_state["intersection topic 2"] = ""
    st.session_state["pd"] = None

def load_examples():
    st.session_state['mesh'] = mesh_term_example.strip()
    st.session_state['subheadings'] = subheading_example.strip()
    st.session_state["proximity topic 1"] = proximity_topic1_example.strip()
    st.session_state["proximity topic 2"] = proximity_topic2_example.strip()
    st.session_state["intersection topic 1"] = intersection_topic1_example.strip()
    st.session_state["intersection topic 2"] = intersection_topic2_example.strip()
    st.session_state["pd"] = 2

st.set_page_config(page_title="Pairwise PubMed Search Generator", page_icon="🔎")
st.title("Pairwise PubMed Search Generator", anchor=False)
st.write("""
This app:
* Generates PubMed search strings from two lists of input terms
* Provides buttons to execute the generated search strings in PubMed in a new browser tab

Use it to:
* Combine a list of MeSH Main Headings with a list of MeSH Subheadings
* Work around the truncation linitation in PubMed's proximity search
* Combine two lists of terms with the AND operator
         
Note:
* A set of example term lists for a search on frailty measures is provided as placeholder text
* Use the **Load example terms** button to load the example terms into the form for search string generation
* The example terms illustrate the order-of-magnitude difference in search results between a proximity search and an intersection search for this topic.
""")

with st.form("enter_terms_form", enter_to_submit=False):
    st.header("Pairwise MeSH Main/Subheading Search", divider=True, anchor=False)
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        mesh_terms = st.text_area(
            label       = "Enter MeSH Main Headings, one per line.", 
            placeholder = mesh_term_example.strip(),
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
            placeholder = subheading_example.strip(),
            height      = text_area_height, 
            key         = "subheadings"
        ).splitlines()
    
    st.header("Pairwise Keyword Proximity Search", divider=True, anchor=False)
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        proximity_topic1_terms = st.text_area(
            label       = "Enter Topic 1 terms, one per line, no truncation.", 
            placeholder = proximity_topic1_example.strip(), 
            height      = text_area_height,
            key         = "proximity topic 1",
        ).splitlines()
        proximity_field = st.selectbox("Proximity field", options=["ti", "tiab", "ad"], index=1)
    with pcol2:                                
        proximity_topic2_terms = st.text_area(
            label       = "Enter Topic 2 terms, one per line, no truncation.", 
            placeholder = proximity_topic2_example.strip(),
            height      = text_area_height, 
            key         = "proximity topic 2",
        ).splitlines()
        proximity_distance = st.number_input("Proximity distance", placeholder=2, key="pd", step=1)

    st.header("Pairwise Keyword Intersection Search (Boolean AND)", divider=True, anchor=False)
    icol1, icol2 = st.columns(2)
    with icol1:
        intersection_topic1_terms = st.text_area(
            label       = "Enter Topic 1 terms, one per line.", 
            placeholder = intersection_topic1_example.strip(),
            height      = text_area_height,
            key         = "intersection topic 1",
        ).splitlines()

    with icol2:                     
        intersection_topic2_terms = st.text_area(
            label       = "Enter Topic 2 terms, one per line.", 
            placeholder = intersection_topic2_example.strip(),
            height      = text_area_height,
            key         = "intersection topic 2"
        ).splitlines() 
    
    st.subheader("Form Controls", divider=True)
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        clear = st.form_submit_button(
            label   = "Clear form inputs",
            on_click = clear_form,
            use_container_width = True,
        )
    with bcol2:
        load_example = st.form_submit_button(
            label = "Load example terms",
            on_click = load_examples,
            use_container_width = True,
        )

    submitted = st.form_submit_button(
        label   = "Generate pairwise search strings and PubMed search buttons",
        use_container_width = True,
    )

    if submitted:
        st.subheader("Generated Search Strings", divider=True)
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
                mesh_search_string
            st.link_button(
                label   = "Search PubMed with pairwise MeSH heading/subheading search string",
                url     = pubmed_search_url+mesh_search_string.replace(" ", "+"),
                type    = "primary",
                use_container_width = True,

            )

        keyword_proximity_searches = [
            f'"{ptopic1_term} {ptopic2_term}"[{proximity_field}:~{proximity_distance}]'
            for ptopic1_term in proximity_topic1_terms
            for ptopic2_term in proximity_topic2_terms
        ]
        keyword_proximity_search_string = " OR ".join(keyword_proximity_searches)
        if keyword_proximity_search_string:
            with st.expander("Pairwise Keyword Proximity Search String"):
                keyword_proximity_search_string

            st.link_button(
                label   = "Search PubMed with pairwise keyword proximity search string",
                url     = pubmed_search_url+keyword_proximity_search_string.replace(" ", "+"),
                type    = "primary",
                use_container_width = True,
            )
            
            if mesh_search_string:
                mesh_proximity_search_string = " OR ".join([mesh_search_string, keyword_proximity_search_string])
                st.link_button(
                    label   = "Search PubMed with combined pairwise MeSH/proximity search strings",
                    url     = pubmed_search_url+mesh_proximity_search_string.replace(" ", "+"),
                    type    = "primary",
                    use_container_width = True,
                )

        keyword_intersection_searches = [
            "(" + itopic1_term + " AND " + itopic2_term + ")"
            for itopic1_term in intersection_topic1_terms
            for itopic2_term in intersection_topic2_terms
        ]
        keyword_intersection_search_string = " OR ".join(keyword_intersection_searches)
        if keyword_intersection_search_string:
            with st.expander("Pairwise Keyword Intersection Search String"):
                keyword_intersection_search_string
        
            st.link_button(
                label   = "Search PubMed with pairwise keyword intersection search string",
                url     = pubmed_search_url+keyword_intersection_search_string.replace(" ", "+"),
                type    = "primary",
                use_container_width = True,
            )

            mesh_intersection_search_string = " OR ".join([mesh_search_string, keyword_intersection_search_string])
            st.link_button(
                label   = "Search PubMed with combined pairwise MeSH/intersection search strings",
                url     = pubmed_search_url+mesh_intersection_search_string.replace(" ", "+"),
                type = "primary",
                use_container_width = True,
            )

        if not (mesh_search_string and keyword_proximity_search_string and keyword_intersection_search_string):
            st.write("Empty form inputs, no search strings generated.")
