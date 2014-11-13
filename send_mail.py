#!/usr/bin/env python
# coding=utf-8

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

from_addr = '834788686@qq.com'
smtp_server = 'smtp.qq.com'
password = raw_input('Pwd: ')
to_addr = raw_input('Send to: ')
title = raw_input("Title: ")
content = raw_input('Content: ')

msg = MIMEText(content, 'plain', 'utf-8')
msg['From'] = _format_addr(u'LY<%s>' % from_addr)
msg['To'] = _format_addr(u'<%s>' % to_addr)
msg['Subject'] = Header(u'%s' % title, 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

