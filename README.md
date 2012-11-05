Notifybot
=========

Dependencies
------------

Notifybot requires xmpppy (packaged as python-xmpp in debian)

Installing
----------

Put notifybot.py somewhere in $PATH (such as /usr/local/bin) and make it executable.

Rename `notifybot.cfg.example` to `notifybot.cfg` and edit it to contain a valid jabberid and password.

The configuration file will be read from the `/etc/notifybot.cfg` or `~/.notifybot.cfg` or `./notifybot.cfg`.

Using
-----

Add notifybot as a notification command (in `/etc/icinga/commands.cfg` for Icinga)

    # 'notify-host-by-xmpp' command definition
    define command{
        command_name    notify-host-by-xmpp
        command_line    /usr/local/bin/notifybot.py $CONTACTEMAIL$ "$NOTIFICATIONTYPE$: $HOSTNAME$ is now $HOSTSTATE$"
        }

    # 'notify-service-by-xmpp' command definition
    define command{
        command_name    notify-service-by-xmpp
        command_line    /usr/local/bin/notifybot.py $CONTACTEMAIL$ "$NOTIFICATIONTYPE$: $HOSTALIAS$/$SERVICEDESC$ is now $SERVICESTATE$: $SERVICEOUTPUT$"
        }  

Add a new XMPP contact (in `/etc/icinga/objects/contacts_icinga.cfg`)

    define contact{
            contact_name                    me-xmpp
            alias                           Me
            service_notification_period     24x7
            host_notification_period        24x7
            service_notification_options    w,u,c,r
            host_notification_options       d,r
            service_notification_commands   notify-service-by-xmpp
            host_notification_commands      notify-host-by-xmpp
            email                           me@jabber.org
            }

Add this contact to a contact group that receives notifications:

    define contactgroup{
        contactgroup_name       admins
        alias                   Nagios Administrators
        members                 me-xmpp
        }
