import smtplib
import streamlit as st

From = "badakabhishek170@gmail.com"
Sub = st.text_input("Enter subject:")
To = st.text_input("Enter receiver's email:")
msg =  st.text_input("Enter message:")

text = f"Subject: {Sub}\n\n{msg}"

if st.button("Send Email"):

  with smtplib.SMTP("smtp.gmail.com",587) as server:
    server.starttls()
<<<<<<< HEAD
    server.login(From,password="vpzp wegb  fodp")
=======
    server.login(From,password="vpzp wegb fodp")
>>>>>>> dcc1c39e8ba34996d74f36d3dc2314b25987ed28
    server.sendmail(from_addr=From,to_addrs=To, msg=text)

    print("Email sent successfully")
    st.success("Email sent successfully")
