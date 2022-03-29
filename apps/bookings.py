import streamlit as st  
import requests
import json
import pandas as pd
import datetime

endpoint = 'https://dc7beo.deta.dev'

def app():
  st.title('会議室予約')

  # ユーザー一覧を取得
  url_users = endpoint + '/users'
  res_user = requests.get(url_users) 
  users = res_user.json()
  # st.write(users)

  users_dict =[]
  for user in users:
    user_dict = {}
    user_dict['name'] = user['name']
    user_dict['age'] = user['age']
    user_dict['hometown'] = user['hometown']
    users_dict.append(user_dict)

  # st.write(users_dict)  
  user_list = pd.DataFrame(users_dict)
 
  st.write('### ユーザー一覧')
  st.table(user_list)

  users_name = {}
  for user in users :
    users_name[user['name']] = user['key']


  # 会議室一覧を取得
  url_rooms = endpoint + '/rooms'
  res_room = requests.get(url_rooms) 
  rooms = res_room.json()

  rooms_dict =[]
  for room in rooms:
    room_dict = {}
    room_dict['room name'] = room['room_name']
    room_dict['capacity'] = room['capacity']
    rooms_dict.append(room_dict)

  # room_list.columns = ['room name','capacity']
  room_list = pd.DataFrame(rooms_dict)

  st.write('### 会議室一覧')
  st.table(room_list)


  

  # 予約一覧を取得
  url_bookings = endpoint + '/bookings'
  res_booking = requests.get(url_bookings) 
  bookings = res_booking.json()
  # booking_list = pd.DataFrame(bookings)
  # st.write(booking_list)

  users_key = {}
  for user in users:
    users_key[user['key']] = user['name']

  rooms_key = {}
  for room in rooms:
    rooms_key[room['key']] = {
      'room_name': room['room_name'],
      'capacity': room['capacity']
    }

  bookings_dict =[]
  for booking in bookings:
    booking_dict = {}
    booking_dict['name'] = users_key[booking['user_key']]
    booking_dict['room name'] = rooms_key[booking['room_key']]['room_name'] 
    booking_dict['reserved num'] = booking['reserved_num']
    booking_dict['start time'] = datetime.datetime.fromisoformat(booking['start_date_time']).strftime('%Y/%m/%d %H:%M') 
    booking_dict['end time'] = datetime.datetime.fromisoformat(booking['end_date_time']).strftime('%Y/%m/%d %H:%M')
    bookings_dict.append(booking_dict)

  booking_list = pd.DataFrame(bookings_dict)  

  # booking_list = booking_list.rename(columns={
  #   'user_key':'予約者名',
  #   'room_key':'会議室名',
  #   'reserved_num':'予約人数',
  #   'start_date_time':'開始時刻',
  #   'end_date_time':'終了時刻',
  #   'key':'予約番号'
  # })

  st.write('### 予約一覧')
  st.table(booking_list)

  room_dict = {}
  for room in rooms :
    room_dict[room['room_name']] = {
      'room_key': room['key'],
      'capacity': room['capacity']
    }
    
  with st.form(key='booking'):
    username: str = st.selectbox('予約者名', users_name.keys())
    roomname: str = st.selectbox('会議室名', room_dict.keys())
    reserved_num: int = st.number_input('予約人数', step=1, min_value=1)
    date = st.date_input('日付を入力', min_value=datetime.date.today())
    start_time = st.time_input('開始時刻: ',value=datetime.time(hour=9, minute=0))
    end_time = st.time_input('終了時刻: ',value=datetime.time(hour=20, minute=0))

    submit_button = st.form_submit_button(label='予約')

  if submit_button:
    user_key: int = users_name[username]
    room_key: int = room_dict[roomname]['room_key']
    capacity: int = room_dict[roomname]['capacity']
    data = {
      'user_key': user_key,
      'room_key': room_key,
      'reserved_num': reserved_num,
      'start_date_time': datetime.datetime(
        year=date.year, 
        month=date.month, 
        day=date.day,
        hour=start_time.hour,
        minute=start_time.minute
      ).isoformat(),
      'end_date_time': datetime.datetime(
        year=date.year, 
        month=date.month, 
        day=date.day,
        hour=end_time.hour,
        minute=end_time.minute
      ).isoformat()
    }
    # 定員以下の場合、予約登録
    if reserved_num > capacity:
      st.error(f'{roomname}の定員は{capacity}名です。') 
    # 開始時刻>=終了時刻
    elif start_time >= end_time:
      st.error('開始時刻が終了時刻を越えています')
    elif start_time < datetime.time(hour=9, minute=0, second=0) or end_time > datetime.time(hour=20, minute=0):
      st.error('利用時間は、9:00～20:00になります。') 
    else:
      url = endpoint + '/bookings'
      res = requests.post(
        url,
        data = json.dumps(data)
      )
      if res.status_code == 200:
        st.success('予約完了しました。')
      # st.write(res.status_code)
      elif res.status_code == 404 and res.json()['detail'] == 'Already booked':
        st.error('指定の時間には既に予約が入っています')
      # st.json(res.json())     