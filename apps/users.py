import streamlit as st  
import requests
import json

endpoint = 'https://dc7beo.deta.dev'


def app():
  st.title('ユーザー登録')

  with st.form(key='user'):
    name: str = st.text_input('ユーザー名', max_chars=12)
    age: int = st.text_input('年齢', max_chars=3)
    hometown: str = st.text_input('出身', max_chars=15)
    data = {
      'name': name,
      'age': age,
      'hometown': hometown
    }
    submit_button = st.form_submit_button(label='登録')

  if submit_button:
    url = endpoint + '/users'
    res = requests.post(
      url,
      data = json.dumps(data)
    )
    if res.status_code == 200:
      st.success('ユーザー登録完了')
    # st.write(res.status_code)
    # st.json(res.json())