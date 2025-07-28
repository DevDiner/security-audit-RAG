### app.py

import streamlit as st
from compliance_rules import check_compliance
from rag_pipeline import create_rag_chain
from streamlit_echarts import st_echarts
import re

st.set_page_config(page_title="RAG Smart Contract Security Audit", layout="wide")
st.title("RAG Smart Contract Security Audit (Web3 Security + LLM RAG)")

st.write("Paste your Solidity smart contract below to check compliance and get AI-powered suggestions.")

code = st.text_area("Paste Solidity contract here:", height=300)

# Gauge chart
def render_gauge(score):
    option = {
        "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
        "series": [
            {
                "name": "Compliance",
                "type": "gauge",
                "progress": {"show": True},
                "detail": {"valueAnimation": True, "formatter": "{value}%"},
                "data": [{"value": score, "name": "Score"}],
                "axisLine": {
                    "lineStyle": {
                        "color": [
                            [0.3, "#FF4C4C"],
                            [0.7, "#FFD700"],
                            [1, "#4CAF50"],
                        ]
                    }
                },
            }
        ],
    }
    st_echarts(option, height="300px")

#  Updated EIP redirected links
EIP_REDIRECTS = {
    "20": "https://github.com/ethereum/ercs/blob/master/ERCS/erc-20.md",
    "721": "https://github.com/ethereum/ercs/blob/master/ERCS/erc-721.md",
    "1155": "https://github.com/ethereum/ercs/blob/master/ERCS/erc-1155.md",
    "897": "https://github.com/ethereum/ercs/blob/master/ERCS/erc-897.md",
    "1822": "https://github.com/ethereum/ercs/blob/master/ERCS/erc-1822.md",
    "1967": "https://github.com/ethereum/ercs/blob/master/ERCS/erc-1967.md",
    "2535": "https://github.com/ethereum/ercs/blob/master/ERCS/erc-2535.md"
}

if st.button("Check Compliance"):
    if not code.strip():
        st.warning("Please paste a contract first!")
    else:
        st.write("### Compliance Analysis")
        score, issues = check_compliance(code)

        st.write(f"**Compliance Score:** {score}/100")
        render_gauge(score)

        if issues:
            st.write("### Issues Detected")
            for issue in issues:
                st.write(f"- {issue['issue']} ({issue['risk']})")

            st.write("### AI Suggestions (with References)")
            st.info("Fetching suggestions and references from knowledge base...")
            qa_chain = create_rag_chain()

            for issue in issues:
                with st.spinner(f"Generating fix for: {issue['issue']}"):
                    result = qa_chain({"query": f"How to fix this issue in Solidity: {issue['issue']}? Provide reference from docs."})
                    suggestion = result["result"]

                    tag = ""
                    docs = result.get("source_documents", [])
                    if docs:
                        ref_text = docs[0].page_content[:200]
                        match = re.search(r"EIP[- ]?(\d+)", ref_text)
                        if match:
                            eip_num = match.group(1)
                            if eip_num in EIP_REDIRECTS:
                                tag = f" ([EIP-{eip_num}]({EIP_REDIRECTS[eip_num]}))"
                            else:
                                tag = f" ([EIP-{eip_num}](https://eips.ethereum.org/EIPS/eip-{eip_num}))"

                    st.markdown(f"**{issue['issue']}** → {suggestion}{tag}")

                    if docs:
                        st.caption(f" Reference snippet: {docs[0].page_content[:200]}...")
        else:
            st.success("Your contract looks compliant with basic checks!")
