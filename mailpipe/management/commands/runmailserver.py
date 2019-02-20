from django.core.management.base import BaseCommand, CommandError
from mailpipe.models import EmailAccount
from mailpipe import tasks
import re
import smtpd
import asyncore
from pprint import pprint
import email


naiveip_re = re.compile(r"""^(?:
(?P<addr>
    (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}) |         # IPv4 address
    (?P<fqdn>[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*) # FQDN
):)?(?P<port>\d+)$""", re.X)


class Command(BaseCommand):
    help = 'Run the mailserver'
    default_addr = '127.0.0.1'
    default_port = 8025

    def add_arguments(self, parser):
        parser.add_argument( 'addrport', nargs='?', help='Optional port number, or ipaddr:port')

    def handle(self, *args, **options):
        if not options['addrport']:
            self.addr = ''
            self.port = self.default_port
        else:
            m = re.match(naiveip_re, options['addrport'])
            if m is None:
                raise CommandError('"%s" is not a valid port number ' 'or address:port pair.' % options['addrport'])
            self.addr, _ipv4, _fqdn, self.port = m.groups()
            if not self.port.isdigit():
                raise CommandError("%r is not a valid port number." % self.port)
        if not self.addr:
            self.addr = self.default_addr



        CustomSMTPServer((self.addr, int(self.port)), None)
        asyncore.loop()

class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, *args, **kwargs):
        print(peer, mailfrom, rcpttos)
        msg = email.message_from_string(data.decode())
        pprint(payload(msg))
        for address in rcpttos:
            tasks.process_email(**{'message':data.decode(), 'address':address})


def payload(msg):
    #  Cache on the instance
    d = {}
    attachments = {}
    for pl in msg.walk():
        if pl.get_filename():
            content_id = pl.get('X-Attachment-Id', None) or pl.get('Content-ID', None)
            filename = pl.get_filename()
            attachments[content_id]= {
                    'filename': filename,
                    'index': len(attachments) + 1,
                    'content_type': pl.get_content_type(),
                    'attachment_url': (content_id),
                    }
        elif pl.get_content_type() in ['text/html', 'text/plain']:
            raw_payload = pl.get_payload()
            if pl.get('Content-Transfer-Encoding') == 'base64':
                raw_payload = base64.b64decode(raw_payload.encode('ascii')).decode('ascii')
            d[pl.get_content_type()] = raw_payload
    d['attachments'] = attachments
    d['to'] = msg['To']
    d['subject'] = msg['subject']
    d['from'] = msg['From']
    d['date'] = msg['date']
    return d





