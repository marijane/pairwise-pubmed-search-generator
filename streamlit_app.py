import streamlit as st

pubmed_search_url = "https://pubmed.ncbi.nlm.nih.gov/?term="

st.set_page_config(page_title="Pairwise PubMed Search Generator")
st.title("Pairwise PubMed Search Generator")

with st.expander("Pairwise Mesh Main Heading/Subheading Search"):
    with st.form("enter_terms_form"):

        mesh_terms = st.text_area("Enter MeSH Main Headings, one per line.", height=300 ,value="asthenia\nfatigue\nfrailty\nmuscle weakness\nmuscle atrophy").splitlines()
        majr = st.checkbox("MeSH Major Topic")
        subheadings = st.text_area("Enter MeSH Subheadings, one per line.", height=200, value="diagnosis\nepidemiology").splitlines()
        submitted = st.form_submit_button("Generate pairwise search string")

    if submitted:
        if majr:
            field = "[majr]"
        else:
            field = "[mh]"
        
        # mesh_term_list = mesh_terms.splitlines()
        # subheading_list = subheadings.splitlines()

        mesh_searches = [
            mesh_term + "/" + subheading + field
            for mesh_term in mesh_terms
            for subheading in subheadings
        ]

        mesh_search_string = " OR ".join(mesh_searches)

        st.write(mesh_search_string)

        st.link_button(label="Search PubMed with pairwise MeSH heading/subheading search string",
                       url=pubmed_search_url+mesh_search_string.replace(" ", "+"))


