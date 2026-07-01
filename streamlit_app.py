import streamlit as st
from groq import Groq

st.set_page_config(page_title="Workout Coach Chatbot", page_icon="💪", layout="centered")

st.title("💪 Workout Coach Chatbot")
st.write(
    "Ask for workout plans, form tips, recovery advice, or anything else fitness-related. "
    "This chatbot is tuned to give practical, safe coaching-style guidance."
)
st.caption("Tip: include your goal, experience level, equipment, and any injuries for better advice.")

groq_api_key = st.text_input("Groq API Key", type="password")
if not groq_api_key:
    st.info("Please add your Groq API key to continue.", icon="🗝️")
else:
    client = Groq(api_key=groq_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        welcome_message = (
            "I’m your workout-focused coaching assistant. I can help with training plans, "
            "exercise selection, form cues, recovery, nutrition basics, and habit-building. "
            "Tell me your goals, experience level, equipment, and schedule and I’ll tailor the advice."
        )
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about workouts, recovery, or form..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = (
            "You are a highly knowledgeable fitness coach. Provide practical, evidence-informed advice "
            "on workouts, strength training, cardio, mobility, recovery, nutrition basics, and habit building. "
            "Be encouraging, specific, and safe. Ask clarifying questions when needed. If the user mentions pain, "
            "injury, or a medical issue, encourage professional guidance and avoid diagnosing. Focus on actionable "
            "steps, progressive overload, realistic expectations, and injury prevention."
        )

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(
            [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
            )
            assistant_reply = response.choices[0].message.content
        except Exception as exc:
            assistant_reply = f"Sorry, I couldn’t get a response from Groq: {exc}"

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
