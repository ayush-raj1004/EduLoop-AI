import streamlit as st
from app.main import run
from app.memory.database import get_recent_runs

st.set_page_config(page_title="EduLoop AI", page_icon="📚", layout="wide")
st.title("📚 EduLoop AI")
st.caption("Self-evaluating agentic lesson content generator")

topic = st.text_input("Enter a lesson topic", value="Introduction to RAG")
if st.button("Generate and evaluate lesson", type="primary"):
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("Generating, evaluating and improving the lesson..."):
            try:
                result = run(topic)
                st.success(f"Workflow finished: {result.get('status')}")
                st.write(f"Attempts: {result.get('attempt')}")
                st.write(f"Run ID: {result.get('run_id')}")
                st.subheader("Evaluation")
                for item in result.get("evaluation", {}).get("checks", []):
                    st.write(
                        f"**{item['check_id']} – {item['name']}: "
                        f"{item['status']}** — {item['reason']}"
                    )
                st.subheader("Rejection history")
                if result.get("rejections"):
                    for rejection in result["rejections"]:
                        with st.expander(f"Attempt {rejection['attempt']}"):
                            st.write(rejection["feedback"])
                else:
                    st.write("No rejected drafts.")
                st.subheader("Final lesson")
                st.markdown(result.get("lesson", "No lesson returned."))
            except Exception as exc:
                st.exception(exc)

st.divider()
st.subheader("Recent runs")
st.dataframe(get_recent_runs(), use_container_width=True)
