#!/usr/bin/env python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

class Email(object):
    def send_email(self):
        sender = 'kb4it.professional@hotmail.com'
        password = 'kAm&STegewA2'
        receiver = 'kb4it.professional@hotmail.com'

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Stock Update'

        msg['From'] = sender
        msg['To'] = receiver

        now = time.strftime("%c")

        text = "Hi there {}".format(now)
        html = """\
        <html>
            <head>
        <title>Stock Update</title>
        <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            text-align: left;
            padding: 8px;
        }
        tr:nth-child(even){background-color: #f2f2f2}
        </style>
        </head>
        <body>
        <div style="overflow-x:auto;">
        <table>
        <tr>
        <th align="justify">SYMBOL</th>
        <th align="justify">Price</th>
        <th align="justify" colspan="2">Today's change</th>
        <th align="justify" colspan="2">1 Week Change</th>
        <th align="justify" colspan="2">1 Month Change</th>
        <th align="justify" colspan="2" >3 Month Change</th>
        <th align="justify" colspan="2">6 Month Change</th>
        <th align="justify" colspan="2">1 Year Change</th>
        </tr>
        <tr>
          <td>AAPL</td>
          <td>160</td>
          <td align="justify" colspan="2">2</td>
          <td align="justify" colspan="2">4</td>
          <td align="justify" colspan="2">3</td>
          <td align="justify" colspan="2">5</td>
          <td align="justify" colspan="2">6</td>
          <td align="justify" colspan="2">4</td>
          </tr>
        </table>
        </div>
        </body>
        </html>
        """

        #html = html.format(now)
        part1 = MIMEText(html, 'html')
        msg.attach(part1)

        s = smtplib.SMTP('smtp.live.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(sender, password)

        s.sendmail(sender, receiver, msg.as_string())
        s.quit()

