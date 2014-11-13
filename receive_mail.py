#!/usr/bin/env python
# coding=utf-8

import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

email = '834788686@qq.com'
password = raw_input('Pwd: ')
pop3_server = 'pop.qq.com'

server = poplib.POP3_SSL(pop3_server)
server.set_debuglevel(1)
print(server.getwelcome())
try:
    server.user(email)
    server.pass_(password)
except poplib.error_proto as e:
    print(e.args[0].decode('gb2312'))
print('Messages: %s. Size: %s' % server.stat())
resp, mails, octets = server.list()
print(mails)
while True:
    choise = raw_input('What do you want? (b): browse email (d):delete email (q):quit ')
    if choise is 'q':
        break
    index = raw_input('Email index: ')
    if choise is 'd':
        resp, lines, octets = server.retr(index)
        server.dele(index)
        print('Messages: %s. Size: %s' % server.stat())
        resp, mails, octets = server.list()
        print(mails)
        continue
    resp, lines, octets = server.retr(index)
    msg_content = '\r\n'.join(lines)
    msg = Parser().parsestr(msg_content)
    print_info(msg)
server.quit()

