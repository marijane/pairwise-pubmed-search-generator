import streamlit as st

pubmed_search_url = "https://pubmed.ncbi.nlm.nih.gov/?term="
text_area_height = 250
collapse_search_string_exp = 1000


# example term lists
mesh_term_example = """
asthenia
fatigue
frailty
muscle weakness
muscle atrophy
""".strip()
subheading_example = """
diagnosis
epidemiology
""".strip()
proximity_topic1_example = """
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
proximity_topic2_example = """
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
intersection_topic1_example = """
asthenia
debilit*
fatigue
frail*
musc* atroph*
musc* wast*
musc* weak*
sarcopenia*
""".strip()
intersection_topic2_example = """
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


# reset form button callback
def reset_form():
    if st.session_state.get("mesh_sh", False):
        st.session_state["mesh_sh"] = False
        st.session_state["majr"] = False
        st.session_state["noexp"] = False
    if st.session_state.get("proximity_kw", False):
        st.session_state["proximity_kw"] = True
        st.session_state["pd"] = 2
        st.session_state["pf"] = "tiab"
    if st.session_state.get("intersection_kw", False):
        st.session_state["intersection_kw"] = False
        st.session_state["sf"] = "tw"
    clear_terms()


# clear text input button callback
def clear_terms():
    # Only clear text inputs for sections that are currently checked
    if st.session_state.get("mesh_sh", False):
        st.session_state["mesh"] = ""
        st.session_state["subheadings"] = ""
    if st.session_state.get("proximity_kw", False):
        st.session_state["proximity topic 1"] = ""
        st.session_state["proximity topic 2"] = ""
    if st.session_state.get("intersection_kw", False):
        st.session_state["intersection topic 1"] = ""
        st.session_state["intersection topic 2"] = ""


# load examples button callback
def load_placeholders():
    # Only load examples for sections that are currently checked
    if st.session_state.get("mesh_sh", False):
        st.session_state["mesh"] = mesh_term_example
        st.session_state["subheadings"] = subheading_example

    if st.session_state.get("proximity_kw", False):
        st.session_state["proximity topic 1"] = proximity_topic1_example
        st.session_state["proximity topic 2"] = proximity_topic2_example
        st.session_state["pd"] = 4
        st.session_state["pf"] = "tiab"

    if st.session_state.get("intersection_kw", False):
        st.session_state["intersection topic 1"] = intersection_topic1_example
        st.session_state["intersection topic 2"] = intersection_topic2_example
        st.session_state["sf"] = "tw"


st.set_page_config(
    page_title="Pairwise PubMed Search Generator",
    page_icon="🔎",
    menu_items={
        "Get help": "mailto:whimar@ohsu.edu",
        "Report a Bug": "https://github.com/marijane/pairwise-pubmed-search-generator/issues",
        "About": "Made by Marijane White with Streamlit",
    },
)
st.html("<h1>Pairwise PubMed Search Generator</h1>")

# info/instructions sidebar
with st.expander(":material/info: Info and Tips", expanded=False):
    st.html("<h2>About</h2>")
    st.write(
        """
The **Pairwise PubMed Search Generator** helps you generate PubMed search strings from two lists of input terms, which can be either copied to your clipboard, or launched in PubMed at the click of a button.

It can save you literally thousands of characters of typing and help you avoid errors in complex search strings.
"""
    )
    st.html("<h2>Features</h2>")
    st.write(
        """
* Combine a list of MeSH Main Headings with a list of MeSH Subheadings
* Quickly generate a PubMed Proximity Search from two lists of search terms
* Combine two lists of search terms with the AND operator (intersection search)
* Combine a pairwise MeSH search with either a pairwise Proximity or Intersection search
"""
    )
    st.html("<h2>Tips</h2>")
    st.write(
        """
* A set of example term lists for a search on *frailty measures* is provided as placeholder text
* Use the **Load placeholder terms** button to load the frailty measures terms into the form for example search string generation
* Use the **Clear terms** button to clear all text inputs without changing other form settings
* Use the **Reset form** button to reset the form to its initial state
"""
)
    st.html("<h2>Caveats</h2>")
    st.write(
        """
* For MeSH Main Heading/subheading searches, make sure the subheadings are valid for all of the MeSH Main Headings entered
* Generated search URLs can be quite long, but it is possible to hit a length limit, which is not documented
* PubMed limits search strings to 256 wildcard (*) characters; if an intersection search string exceeds this limit, a warning message will be shown
"""
    )

st.html(
    """
<h2>What kind of search string do you want to generate?</h2>
<h3>Select all that apply:</h3>
        """
)
mesh_sh = st.checkbox(
    label="Combine a list of [MeSH main headings](https://pubmed.ncbi.nlm.nih.gov/help/#using-mesh-database)  with a list of MeSH subheadings",
    key="mesh_sh",
    # help="Check this box to generate a pairwise MeSH Main Heading/Subheading search string.",
)
proximity_kw = st.checkbox(
    label="Combine two lists of search terms in a [Proximity Search](https://pubmed.ncbi.nlm.nih.gov/help/#proximity-searching)",
    key="proximity_kw",
    # help="Check this box to generate a pairwise proximity search string.",
    value=True,
)
intersection_kw = st.checkbox(
    label="Combine two lists of search terms with the [Boolean](https://pubmed.ncbi.nlm.nih.gov/help/#combining-with-boolean-operators) AND operator",
    key="intersection_kw",
    # help="Check this box to generate a pairwise intersection search string.",
)

with st.form("enter_terms_form", enter_to_submit=False):

    if not (mesh_sh or proximity_kw or intersection_kw):
        st.error("Please select at least one type of search string to generate.")

    if mesh_sh:
        st.html("<h2>Pairwise MeSH Main/Subheading Search</h2>")
        mcol1, mcol2 = st.columns(2)
        with mcol1:
            mesh_terms = st.text_area(
                height=text_area_height,
                key="mesh",
                label="Enter MeSH Main Headings, one per line.",
                placeholder=mesh_term_example,
            ).splitlines()

        with mcol2:
            subheadings = st.text_area(
                height=text_area_height,
                key="subheadings",
                label="Enter MeSH Subheadings, one per line.",
                placeholder=subheading_example,
            ).splitlines()
        moptcol1, moptcol2 = st.columns(2)
        with moptcol1:
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                majr = st.checkbox(
                    "MeSH Major Topic",
                    key="majr",
                )
            with subcol2:
                noexp = st.checkbox("Do not explode", key="noexp")

    if proximity_kw:
        st.html("<h2>Pairwise Proximity Search</h2>")
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            proximity_topic1_terms = st.text_area(
                height=text_area_height,
                key="proximity topic 1",
                label="Enter Topic 1 terms, one per line, no truncation.",
                placeholder=proximity_topic1_example,
            ).splitlines()
            if any("*" in term for term in proximity_topic1_terms):
                st.warning("Wildcards are not allowed in proximity searches.")
        with pcol2:
            proximity_topic2_terms = st.text_area(
                height=text_area_height,
                key="proximity topic 2",
                label="Enter Topic 2 terms, one per line, no truncation.",
                placeholder=proximity_topic2_example,
            ).splitlines()
            if any("*" in term for term in proximity_topic2_terms):
                st.warning("Wildcards are not allowed in proximity searches.")
        poptcol1, poptcol2 = st.columns(2)
        with poptcol1:
            proximity_field = st.selectbox(
                label="Proximity field",
                options=["ti", "tiab", "ad"],
                key="pf",
                index=1,
            )
        with poptcol2:
            proximity_distance = st.number_input(
                key="pd",
                label="Proximity distance",
                min_value=0,
                step=1,
                value=2,
            )

    if intersection_kw:
        st.html("<h2>Pairwise Intersection Search (Boolean AND)</h2>")
        icol1, icol2 = st.columns(2)
        with icol1:
            intersection_topic1_terms = st.text_area(
                height=text_area_height,
                key="intersection topic 1",
                label="Enter Topic 1 terms, one per line.",
                placeholder=intersection_topic1_example,
            ).splitlines()

        with icol2:
            intersection_topic2_terms = st.text_area(
                height=text_area_height,
                key="intersection topic 2",
                label="Enter Topic 2 terms, one per line.",
                placeholder=intersection_topic2_example,
            ).splitlines()

        search_field = st.selectbox(
            label="Search field",
            key="sf",
            options=["ti", "tiab", "tw", "all"],
            index=1,
        )

    st.divider()
    st.form_submit_button(
        label="Load placeholder terms",
        icon=":material/convert_to_text:",
        on_click=load_placeholders,
        use_container_width=True,
    )

    bcol1, bcol2 = st.columns(2)
    with bcol1:
        st.form_submit_button(
            label="Clear terms",
            icon=":material/delete_sweep:",
            on_click=clear_terms,
            use_container_width=True,
        )
    with bcol2:
        st.form_submit_button(
            label="Reset form",
            icon=":material/reset_settings:",
            on_click=reset_form,
            use_container_width=True,
        )

    submitted = st.form_submit_button(
        label="Generate search strings",
        icon=":material/play_circle:",
        use_container_width=True,
        type="primary",
    )

    if submitted:
        if (
            (mesh_sh and mesh_terms and subheadings)
            or (proximity_kw and proximity_topic1_terms and proximity_topic2_terms)
            or (
                intersection_kw
                and intersection_topic1_terms
                and intersection_topic2_terms
            )
        ):

            st.html("<h2>Generated Search Strings</h2>")

            mesh_search_string = ""
            if mesh_sh and mesh_terms and subheadings:
                st.html("<h3>Pairwise MeSH Main/Subheading</h3>")
                mesh_terms_rows = len(mesh_terms)
                subheadings_rows = len(subheadings)
                total_mesh_sh_pairs = mesh_terms_rows * subheadings_rows

                mesh_terms_chars = sum(len(term) for term in mesh_terms)
                subheadings_chars = sum(len(subheading) for subheading in subheadings)
                total_mesh_sh_chars = mesh_terms_chars + subheadings_chars

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
                mesh_search_string_len = len(mesh_search_string)
                mesh_search_string_exp = (
                    mesh_search_string_len < collapse_search_string_exp
                )
                if mesh_search_string:
                    with st.expander(
                        f"Search String (length:{mesh_search_string_len} characters)",
                        expanded=mesh_search_string_exp,
                    ):
                        st.code(mesh_search_string, wrap_lines=True)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("MeSH main headings", value=f"{mesh_terms_rows}", border=True)
                    with col2:
                        st.metric("Subheadings", value=f"{subheadings_rows}", border=True)
                    with col3:
                        st.metric("Total pairs", value=f"{total_mesh_sh_pairs}", border=True)
                    col4, col5 = st.columns(2)
                    with col4:
                        st.metric("Characters typed", value=f"{total_mesh_sh_chars}", border=True)
                    with col5:
                        st.metric(
                            "Characters generated", value=f"{mesh_search_string_len - total_mesh_sh_chars}", border=True
                        )
                    st.link_button(
                        label="Search PubMed with pairwise MeSH heading/subheading search string",
                        type="primary",
                        url=pubmed_search_url + mesh_search_string.replace(" ", "+"),
                        use_container_width=True,
                    )

            if proximity_kw and proximity_topic1_terms and proximity_topic2_terms:
                st.html("<h3>Pairwise Proximity</h3>")
                proximity_topic1_rows = len(proximity_topic1_terms)
                proximity_topic2_rows = len(proximity_topic2_terms)
                total_proximity_pairs = proximity_topic1_rows * proximity_topic2_rows

                proximity_topic1_terms_chars = sum(len(term) for term in proximity_topic1_terms)
                proximity_topic2_terms_chars = sum(len(term) for term in proximity_topic2_terms)
                total_proximity_chars = proximity_topic1_terms_chars + proximity_topic2_terms_chars
                keyword_proximity_searches = [
                    f'"{ptopic1_term} {ptopic2_term}"[{proximity_field}:~{proximity_distance}]'
                    for ptopic1_term in proximity_topic1_terms
                    for ptopic2_term in proximity_topic2_terms
                ]
                keyword_proximity_search_string = " OR ".join(
                    keyword_proximity_searches
                )
                keyword_proximity_search_string_len = len(
                    keyword_proximity_search_string
                )
                keyword_proximity_search_string_exp = (
                    keyword_proximity_search_string_len < collapse_search_string_exp
                )

                if keyword_proximity_search_string:
                    with st.expander(
                        f"Search String (length: {len(keyword_proximity_search_string)} characters)",
                        expanded=keyword_proximity_search_string_exp,
                    ):
                        st.code(
                            keyword_proximity_search_string,
                            wrap_lines=True,
                        )

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Topic 1 terms", value=f"{proximity_topic1_rows}", border=True)
                    with col2:
                        st.metric("Topic 2 terms", value=f"{proximity_topic2_rows}", border=True)
                    with col3:
                        st.metric("Total pairs", value=f"{total_proximity_pairs}", border=True)
                    col4, col5 = st.columns(2)
                    with col4:
                        st.metric(
                            "Characters typed",
                            value=f"{total_proximity_chars}",
                            border=True
                        )
                    with col5:
                        st.metric(
                            "Characters generated",
                            value=f"{keyword_proximity_search_string_len - total_proximity_chars}",
                            border=True
                        )
                    st.link_button(
                        label="Search PubMed with pairwise keyword proximity search string",
                        type="primary",
                        url=pubmed_search_url
                        + keyword_proximity_search_string.replace(" ", "+"),
                        use_container_width=True,
                    )

                    if mesh_search_string:
                        st.html("<h4>MeSH + Proximity</h4>")
                        mesh_proximity_search_string = " OR ".join(
                            [mesh_search_string, keyword_proximity_search_string]
                        )
                        mesh_proximity_search_string_len = len(
                            mesh_proximity_search_string
                        )
                        mesh_proximity_search_string_exp = (
                            mesh_proximity_search_string_len
                            < collapse_search_string_exp
                        )

                        with st.expander(
                            f"Union (Boolean OR) with MeSH search string (length: {len(mesh_proximity_search_string)} characters)",
                            expanded=keyword_proximity_search_string_exp,
                        ):
                            st.code(
                                mesh_proximity_search_string,
                                wrap_lines=True,
                            )

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total pairs", value=f"{total_mesh_sh_pairs + total_proximity_pairs}", border=True)
                        with col2:
                            st.metric(
                                "Characters typed",
                                value=f"{total_mesh_sh_chars + total_proximity_chars}",
                                border=True,
                            )
                        with col3:
                            st.metric(
                                "Characters generated",
                                value=f"{mesh_proximity_search_string_len - (total_mesh_sh_chars + total_proximity_chars)}",
                                border=True,
                            )
                        st.link_button(
                            label="Search PubMed with union of pairwise MeSH/proximity search strings",
                            url=pubmed_search_url
                            + mesh_proximity_search_string.replace(" ", "+"),
                            use_container_width=True,
                        )

            if (
                intersection_kw
                and intersection_topic1_terms
                and intersection_topic2_terms
            ):
                st.html("<h3>Pairwise Intersection</h3>")
                intersection_topic1_rows = len(intersection_topic1_terms)
                intersection_topic2_rows = len(intersection_topic2_terms)
                total_intersection_pairs = intersection_topic1_rows * intersection_topic2_rows

                intersection_topic1_terms_chars = sum(len(term) for term in intersection_topic1_terms)
                intersection_topic2_terms_chars = sum(len(term) for term in intersection_topic2_terms)
                total_intersection_chars = intersection_topic1_terms_chars + intersection_topic2_terms_chars

                keyword_intersection_searches = [
                    f"({itopic1_term}[{search_field}] AND {itopic2_term}[{search_field}])"
                    for itopic1_term in intersection_topic1_terms
                    for itopic2_term in intersection_topic2_terms
                ]
                keyword_intersection_search_string = " OR ".join(
                    keyword_intersection_searches
                )
                if keyword_intersection_search_string.count("*") > 256:
                    st.warning(
                        "The generated search string contains more than 256 wildcard (*) characters, which exceeds PubMed's limit. Please edit the input term lists and try again."
                    )
                keyword_intersection_search_string_len = len(
                    keyword_intersection_search_string
                )
                keyword_intersection_search_string_exp = (
                    keyword_intersection_search_string_len < collapse_search_string_exp
                )
                if keyword_intersection_search_string:
                    with st.expander(
                        f"Search String (length: {len(keyword_intersection_search_string)} characters)",
                        expanded=keyword_intersection_search_string_exp,
                    ):
                        st.code(
                            keyword_intersection_search_string,
                            wrap_lines=True,
                        )

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Topic 1 terms", value=f"{intersection_topic1_rows}", border=True)
                    with col2:
                        st.metric("Topic 2 terms", value=f"{intersection_topic2_rows}", border=True)
                    with col3:
                        st.metric("Total pairs", value=f"{total_intersection_pairs}", border=True)
                    col4, col5 = st.columns(2)
                    with col4:
                        st.metric(
                            "Characters typed",
                            value=f"{total_intersection_chars}",
                            border=True
                        )
                    with col5:
                        st.metric(
                            "Characters generated",
                            value=f"{keyword_intersection_search_string_len - total_intersection_chars}",
                            border=True
                        )

                    st.link_button(
                        label="Search PubMed with pairwise keyword intersection search string",
                        type="primary",
                        url=pubmed_search_url
                        + keyword_intersection_search_string.replace(" ", "+"),
                        use_container_width=True,
                    )

                    if mesh_search_string:
                        st.html("<h4>MeSH + Intersection</h4>")
                        mesh_intersection_search_string = " OR ".join(
                            [mesh_search_string, keyword_intersection_search_string]
                        )
                        mesh_intersection_search_string_len = len(
                            mesh_intersection_search_string
                        )
                        mesh_intersection_search_string_exp = (
                            mesh_intersection_search_string_len
                            < collapse_search_string_exp
                        )
                        with st.expander(
                            f"Union (Boolean OR) with MeSH search string (length: {len(mesh_intersection_search_string)} characters, wildcard count: {keyword_intersection_search_string.count('*')})",
                            expanded=keyword_intersection_search_string_exp,
                        ):

                            st.code(mesh_intersection_search_string, wrap_lines=True)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(
                                "Total pairs",
                                value=f"{total_mesh_sh_pairs + total_intersection_pairs}",
                                border=True
                            )
                        with col2:
                            st.metric(
                                "Characters typed",
                                value=f"{total_mesh_sh_chars + total_intersection_chars}",
                                border=True
                            )
                        with col3:
                            st.metric(
                                "Characters generated",
                                value=f"{mesh_intersection_search_string_len - (total_mesh_sh_chars + total_intersection_chars)}",
                                border=True
                            )

                        st.link_button(
                            label="Search PubMed with union of pairwise MeSH/intersection search strings",
                            url=pubmed_search_url
                            + mesh_intersection_search_string.replace(" ", "+"),
                            use_container_width=True,
                        )
        else:
            st.error(
                "Empty form inputs, no search strings generated.\n\n**Tip**: Use the *Load placeholder terms* button to load example terms into the form before generating search strings."
            )
