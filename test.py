import smtplib

EMAIL = "mit026661@gmail.com"
PASSWORD = "xwsxkunamhmoyhdn"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(EMAIL, PASSWORD)

print("Login successful")
server.quit()