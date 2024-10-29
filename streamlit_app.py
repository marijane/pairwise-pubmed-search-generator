import streamlit as st

pubmed_search_url = "https://pubmed.ncbi.nlm.nih.gov/?term="
text_area_height = 250

# example term lists
mesh_term_example = \
"""
asthenia
fatigue
frailty
muscle weakness
muscle atrophy
""".strip()
subheading_example = \
"""
diagnosis
epidemiology
""".strip()
proximity_topic1_example = \
"""
asthenia
debility
fatigue
frailty
muscle weakness
muscular weakness
muscle atrophy
muscular atrophy
sarcopenia
""".strip()
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
indices
measure
measures
scale
scales
score
scores
scoring
screen
screens
screening
screenings
test
tests
testing
tool
tools
""".strip()
intersection_topic1_example = \
"""
asthenia
debilit*
fatigue
frail*
musc* atroph*
musc* wast*
musc* weak*
sarcopenia*
""".strip()
intersection_topic2_example = \
"""
assess*
diagnos*
evaluat*
index
indic*
instrument*
measure*
scale*
score*
screen*
test*
tool*
""".strip()

# clear form button callback
def clear_form():
    st.session_state["mesh"] = ""
    st.session_state["subheadings"] = ""
    st.session_state["proximity topic 1"] = ""
    st.session_state["proximity topic 2"] = ""
    st.session_state["intersection topic 1"] = ""
    st.session_state["intersection topic 2"] = ""
    st.session_state["pd"] = 2
    st.session_state["pf"] = "tiab"
    st.session_state["sf"] = "tw"
    st.session_state["majr"] = False
    st.session_state["noexp"] = False

# load examples button callback
def load_examples():
    st.session_state['mesh'] = mesh_term_example
    st.session_state['subheadings'] = subheading_example
    st.session_state["proximity topic 1"] = proximity_topic1_example
    st.session_state["proximity topic 2"] = proximity_topic2_example
    st.session_state["intersection topic 1"] = intersection_topic1_example
    st.session_state["intersection topic 2"] = intersection_topic2_example
    st.session_state["pd"] = 4
    st.session_state["pf"] = "tiab"
    st.session_state["sf"] = "tw"
    
st.set_page_config(
    page_title  = "Pairwise PubMed Search Generator", 
    page_icon   = "🔎",
    menu_items  = {
        "Get help":"mailto:whimar@ohsu.edu", 
        "Report a Bug":"https://github.com/marijane/pairwise-pubmed-search-generator/issues",
        "About": "Made by Marijane White with Streamlit",
    }
)
st.title("Pairwise PubMed Search Generator", anchor=False)

# info/instructions sidebar
with st.sidebar:
    st.write("""
This app:
* Generates PubMed search strings from two lists of input terms, which can be easily copied to your clipboard
* Provides buttons to execute the generated search strings in PubMed in a new browser tab

Use it to:
* Combine a list of MeSH Main Headings with a list of MeSH Subheadings
* Work around the truncation linitation in PubMed's proximity search
* Combine two lists of terms with the AND operator
         
Note:
* A set of example term lists for a search on *frailty measures* is provided as placeholder text
* Use the :red[Load example terms] button to load the frailty measures terms into the form for search string generation
* Generated search URLs can be quite long, but it is possible to hit a length limit, which is not documented
* A PubMed search can have no more than 256 wildcard characters
""")

with st.form("enter_terms_form", enter_to_submit=False):
    st.header("Pairwise MeSH Main/Subheading Search", divider=True, anchor=False)
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        mesh_terms = st.text_area(
            height      = text_area_height,
            key         = "mesh",
            label       = "Enter MeSH Main Headings, one per line.", 
            placeholder = mesh_term_example,
        ).splitlines()

        subcol1, subcol2 = st.columns(2)
        with subcol1:
            majr = st.checkbox("MeSH Major Topic", key="majr")
        with subcol2:
            noexp = st.checkbox("Do not explode", key="noexp")

    with mcol2:
        subheadings = st.text_area(
            height      = text_area_height, 
            key         = "subheadings",
            label       = "Enter MeSH Subheadings, one per line.", 
            placeholder = subheading_example,
        ).splitlines()
    
    st.header("Pairwise Keyword Proximity Search", divider=True, anchor=False)
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        proximity_topic1_terms = st.text_area(
            height      = text_area_height,
            key         = "proximity topic 1",
            label       = "Enter Topic 1 terms, one per line, no truncation.", 
            placeholder = proximity_topic1_example, 
        ).splitlines()
        proximity_field = st.selectbox(
            index=1,
            key="pf",
            label="Proximity field", 
            options=["ti", "tiab", "ad"], 
        )
    with pcol2:                                
        proximity_topic2_terms = st.text_area(
            height      = text_area_height, 
            key         = "proximity topic 2",
            label       = "Enter Topic 2 terms, one per line, no truncation.", 
            placeholder = proximity_topic2_example,
        ).splitlines()
        proximity_distance = st.number_input(
            key         = "pd", 
            label       = "Proximity distance", 
            min_value   = 0, 
            step        = 1,
            value       = 2, 
        )

    st.header("Pairwise Keyword Intersection Search (Boolean AND)", divider=True, anchor=False)
    icol1, icol2 = st.columns(2)
    with icol1:
        intersection_topic1_terms = st.text_area(
            height      = text_area_height,
            key         = "intersection topic 1",
            label       = "Enter Topic 1 terms, one per line.", 
            placeholder = intersection_topic1_example,
        ).splitlines()

    with icol2:                     
        intersection_topic2_terms = st.text_area(
            height      = text_area_height,
            key         = "intersection topic 2",
            label       = "Enter Topic 2 terms, one per line.", 
            placeholder = intersection_topic2_example,
        ).splitlines()

    search_field = st.selectbox(
        index   = 2,
        label   = "Search field", 
        key     = "sf",
        options = ["ti", "tiab", "tw", "all"], 
    )
    
    st.divider()
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        clear = st.form_submit_button(
            label               = "Clear form inputs",
            on_click            = clear_form,
            use_container_width = True,
        )
    with bcol2:
        load_example = st.form_submit_button(
            label               = "Load example terms",
            on_click            = load_examples,
            use_container_width = True,
        )

    submitted = st.form_submit_button(
        label   = "Generate pairwise search strings and PubMed search buttons",
        use_container_width = True,
    )

    if submitted:
        if not (mesh_terms and proximity_topic1_terms and intersection_topic1_terms):
            st.write("Empty form inputs, no search strings generated.")
        else:

            st.header("Generated Search Strings", divider=True, anchor=False)
            
            st.subheader("Pairwise MeSH Main/Subheading", divider=True, anchor=False)
            if majr:
                field = "majr"
            else:
                field = "mh"
            if noexp:
                field = field + ":noexp"
            mesh_searches = [
                f"{mesh_term}/{subheading}[{field}]"
                for mesh_term in mesh_terms
                for subheading in subheadings
            ]
            mesh_search_string = " OR ".join(mesh_searches)
            if mesh_search_string: 
                with st.expander("Search String", expanded=True):
                    st.code(mesh_search_string, language="python", wrap_lines=True)
                st.link_button(
                    label               = "Search PubMed with pairwise MeSH heading/subheading search string",
                    type                = "primary",
                    url                 = pubmed_search_url+mesh_search_string.replace(" ", "+"),
                    use_container_width = True,
                )

            st.subheader("Pairwise Keyword Proximity", divider=True, anchor=False)
            keyword_proximity_searches = [
                f'"{ptopic1_term} {ptopic2_term}"[{proximity_field}:~{proximity_distance}]'
                for ptopic1_term in proximity_topic1_terms
                for ptopic2_term in proximity_topic2_terms
            ]
            keyword_proximity_search_string = " OR ".join(keyword_proximity_searches)
            if keyword_proximity_search_string:
                with st.expander(f"Search String (length: {len(keyword_proximity_search_string)} characters)"):
                    st.code(keyword_proximity_search_string, language="python", wrap_lines=True)
                st.link_button(
                    label               = "Search PubMed with pairwise keyword proximity search string",
                    type                = "primary",
                    url                 = pubmed_search_url+keyword_proximity_search_string.replace(" ", "+"),
                    use_container_width = True,
                )
                
                if mesh_search_string:
                    mesh_proximity_search_string = " OR ".join([mesh_search_string, keyword_proximity_search_string])
                    with st.expander(f"Union (Boolean OR) with MeSH search string (length: {len(mesh_proximity_search_string)} characters)"):
                        st.code(mesh_proximity_search_string, language="python", wrap_lines=True)
                    st.link_button(
                        label               = "Search PubMed with union of pairwise MeSH/proximity search strings",
                        url                 = pubmed_search_url+mesh_proximity_search_string.replace(" ", "+"),
                        use_container_width = True,
                    )

            st.subheader("Pairwise Keyword Intersection", divider=True, anchor=False)

            keyword_intersection_searches = [
                f"({itopic1_term}[{search_field}] AND {itopic2_term}[{search_field}])"
                for itopic1_term in intersection_topic1_terms
                for itopic2_term in intersection_topic2_terms
            ]
            keyword_intersection_search_string = " OR ".join(keyword_intersection_searches)
            if keyword_intersection_search_string:
                with st.expander(f"Search String (length: {len(keyword_intersection_search_string)} characters, wildcard count: {keyword_intersection_search_string.count('*')})"):
                    st.code(keyword_intersection_search_string, language="python", wrap_lines=True)
            
                st.link_button(
                    label               = "Search PubMed with pairwise keyword intersection search string",
                    type                = "primary",
                    url                 = pubmed_search_url+keyword_intersection_search_string.replace(" ", "+"),
                    use_container_width = True,
                )

                mesh_intersection_search_string = " OR ".join([mesh_search_string, keyword_intersection_search_string])
                with st.expander(f"Union (Boolean OR) with MeSH search string (length: {len(mesh_intersection_search_string)} characters, wildcard count: {keyword_intersection_search_string.count('*')})"):
                    st.code(mesh_intersection_search_string, language="python", wrap_lines=True)

                st.link_button(
                    label               = "Search PubMed with union of pairwise MeSH/intersection search strings",
                    url                 = pubmed_search_url+mesh_intersection_search_string.replace(" ", "+"),
                    use_container_width = True,
                )

