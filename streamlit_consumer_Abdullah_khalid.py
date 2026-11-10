import time
import json
import uuid
import streamlit as st
import pandas as pd
from kafka import KafkaConsumer
from poll_response_api import PollResponseAPI

st.set_page_config(page_title="Live Poll Dashboard", layout="wide")

TOPIC_NAME = 'poll_responses_v2' 
BOOTSTRAP_SERVERS = ['localhost:9092']
YOUR_NAME = "Abdullah Khalid Khan"

api = PollResponseAPI()
questions = api.survey_questions
q1_text, q1_options = questions[0]['Q'], questions[0]['A']
q2_text, q2_options = questions[1]['Q'], questions[1]['A']
q3_text, q3_options = questions[2]['Q'], questions[2]['A']

@st.cache_resource
def get_consumer():
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=f'abdullah-v2-{uuid.uuid4().hex[:6]}',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=500
    )
consumer = get_consumer()

if 'poll_records' not in st.session_state:
    st.session_state.poll_records = []

messages = consumer.poll(timeout_ms=300, max_records=1)

for tp, msg_list in messages.items():
    for msg in msg_list:
        payload = msg.value
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                continue

        ans_array = payload.get('answer_array', [])
        
        ans1 = list(ans_array[0].values())[0] if len(ans_array) > 0 else None
        ans2 = list(ans_array[1].values())[0] if len(ans_array) > 1 else None
        ans3 = list(ans_array[2].values())[0] if len(ans_array) > 2 else None

        st.session_state.poll_records.append({
            'answer_id': payload.get('answer_id'),
            'Q1': str(ans1).strip() if ans1 is not None else None,
            'Q2': str(ans2).strip() if ans2 is not None else None,
            'Q3': str(ans3).strip() if ans3 is not None else None
        })

if st.session_state.poll_records:
    df = pd.DataFrame(st.session_state.poll_records)
else:
    df = pd.DataFrame(columns=['answer_id', 'Q1', 'Q2', 'Q3'])

st.title("📊 Live Event Poll Dashboard")

st.metric(label="Total Responses Received", value=len(df))

def get_chart_data(series, options_order):
    counts = series.value_counts() if not series.empty else pd.Series(dtype=int)
    reindexed = counts.reindex(options_order, fill_value=0)
    return pd.DataFrame({'Options': options_order, 'Votes': reindexed.values}).set_index('Options')

st.subheader(f"Question 1: {q1_text}")
st.bar_chart(get_chart_data(df['Q1'], q1_options))

st.subheader(f"Question 2: {q2_text}")
st.bar_chart(get_chart_data(df['Q2'], q2_options))

st.subheader(f"Question 3: {q3_text}")
st.bar_chart(get_chart_data(df['Q3'], q3_options))

st.subheader("📋 Response Feed (DataFrame)")
st.dataframe(df.tail(20), use_container_width=True)

st.markdown(
    f"<hr><p style='text-align: center; color: gray;'>App created by <b>{YOUR_NAME}</b></p>",
    unsafe_allow_html=True
)

time.sleep(1)
st.rerun()