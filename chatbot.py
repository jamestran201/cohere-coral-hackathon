import cohere
import os
import streamlit as st

CONNECTOR_ID = os.environ.get("COHERE_CONNECTOR_ID")

co = cohere.Client(os.environ.get("COHERE_API_KEY"))

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by Cohere Coral")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_prompt := st.chat_input("What was the root cause for the incident at Atlassian?"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    response = co.chat(message=user_prompt, temperature=0, connectors=[{"id": CONNECTOR_ID}])
    with st.chat_message("assistant"):
        annotated_text = response.text
        offset = 0
        max_ref_number = 0
        doc_id_to_ref_number = {}

        for citation in response.citations:
            reference_numbers = []
            for doc_id in citation["document_ids"]:
                if doc_id in doc_id_to_ref_number:
                    reference_numbers.append(doc_id_to_ref_number[doc_id])
                    continue
                
                max_ref_number += 1
                reference_numbers.append(str(max_ref_number))
                doc_id_to_ref_number[doc_id] = str(max_ref_number)

            index = citation["end"] + offset
            annotation = f" [Ref {', '.join(reference_numbers)}]"
            

            annotated_text = annotated_text[:index] + annotation + annotated_text[index:]
            offset += len(annotation)

        st.write(annotated_text)
        
        for doc_id, ref_number in doc_id_to_ref_number.items():
            with st.expander(f"Reference {ref_number}"):
                for doc in response.documents:
                    if doc["id"] != doc_id:
                        continue

                    st.markdown(doc["snippet"])
                    st.write(f"Incident review: {doc['url']}")
                    break