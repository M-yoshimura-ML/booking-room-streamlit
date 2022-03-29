import streamlit as st
from multiapp import MultiApp
from apps import users, rooms, bookings # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("users", users.app)
app.add_app("rooms", rooms.app)
app.add_app("bookings", bookings.app)

# The main app
app.run()



 
