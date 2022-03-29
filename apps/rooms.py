import streamlit as st  
import requests
import json

endpoint = 'https://dc7beo.deta.dev'

def app():
  st.title('会議室登録')

  with st.form(key='room'):
    room_name: str = st.text_input('会議室名', max_chars=12)
    capacity: int = st.number_input('定員', step=1)
    data = {
      'room_name': room_name,
      'capacity': capacity
    }
    submit_button = st.form_submit_button(label='登録')

  if submit_button:
    url = endpoint + '/rooms'
    res = requests.post(
      url,
      data = json.dumps(data)
    )
    if res.status_code == 200:
      st.success('会議室登録完了')
    
    # st.write(res.status_code)
    # st.json(res.json())