#!/usr/bin/python
import sys,os,time
import xmpp
import ConfigParser

def print_usage():
    print "Syntax: notifybot.py jabberid message"
    sys.exit(0)

def read_config():
    filenames = [
        '/etc/notifybot.cfg',
        os.path.expanduser('~/.notifybot.cfg'),
        'notifybot.cfg'
    ]

    config = ConfigParser.SafeConfigParser()

    if not config.read(filenames):
        print 'Unable to locate notifybot.cfg'
        sys.exit()

    return config

def main():
    tojid = sys.argv[1]
    text = ' '.join(sys.argv[2:])

    config = read_config()
  
    jid = xmpp.protocol.JID(config.get('xmpp', 'jid'))
    cl  = xmpp.Client(jid.getDomain(), debug=[])
  
    con = cl.connect()
    if not con:
        print 'Error connecting'
        sys.exit()

    auth = cl.auth(jid.getNode(), config.get('xmpp', 'password'), resource=jid.getResource())
    if not auth:
        print 'Error authenticating'
        sys.exit()
  
    id = cl.send(xmpp.protocol.Message(tojid, text))
    if not id:
        print 'Error sending message'
    else:
        print 'sent message with id', id
  
    time.sleep(1)   # some older servers will not send the message if you disconnect immediately after sending

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()

    main()

# vim: set smartindent shiftwidth=4 tabstop=4 softtabstop=4 expandtab :
