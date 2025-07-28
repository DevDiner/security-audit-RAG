import streamlit as st
from compliance_rules import check_compliance
from rag_pipeline import create_rag_chain
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Smart Contract Compliance Checker", layout="wide")
st.title("🔍 Smart Contract Compliance Checker (AI + RAG)")

st.write("Paste your Solidity smart contract below to check compliance and get AI-powered suggestions.")

code = st.text_area("Paste Solidity contract here:", height=300)

# ✅ Gauge chart
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
                            [0.3, "#FF4C4C"],  # Red
                            [0.7, "#FFD700"],  # Yellow
                            [1, "#4CAF50"],    # Green
                        ]
                    }
                },
            }
        ],
    }
    st_echarts(option, height="300px")

if st.button("Check Compliance"):
    if not code.strip():
        st.warning("Please paste a contract first!")
    else:
        st.write("### ✅ Compliance Analysis")
        score, issues = check_compliance(code)

        st.write(f"**Compliance Score:** {score}/100")
        render_gauge(score)

        if issues:
            st.write("### ❌ Issues Detected")
            for issue in issues:
                st.write(f"- {issue['issue']} ({issue['risk']})")

            st.write("### 💡 AI Suggestions (with References)")
            st.info("Fetching suggestions and references from knowledge base...")
            qa_chain = create_rag_chain()

            for issue in issues:
                with st.spinner(f"Generating fix for: {issue['issue']}"):
                    result = qa_chain({"query": f"How to fix this issue in Solidity: {issue['issue']}? Provide reference from docs."})
                    suggestion = result["result"]

                    st.markdown(f"**{issue['issue']}** → {suggestion}")

                    # ✅ Show retrieved references
                    retrieved_docs = result.get("source_documents", [])
                    if retrieved_docs:
                        st.caption(f"📚 Reference snippet: {retrieved_docs[0].page_content[:200]}...")
        else:
            st.success("Your contract looks compliant with basic checks!")
