import argparse


parser = argparse.ArgumentParser(description='''InstaTorCloud -- Launch a
                                     Tor Bridge running on an EC2 instance in
                                     a single command.''')

parser.add_argument('-v', '--version', action='version',
                     version='InstaTorCloud v0.1')

parser.add_argument('--access-key-id', '-a', dest='akid',
                    help='''Where you must insert your AWS Access Key ID.
                    (More info here: http://goo.gl/fCVGi)''',
                    required=True)
parser.add_argument('--secret-access-key', '-s', dest='sak',
                    help='''Where you must insert your AWS Secret Access Key.
                    (More info here: http://goo.gl/fCVGi)''',
                    required=True)

parser.add_argument('--security-group', dest='secgrp',
                    help='''Name of the Security Group
                    you want to use for the instance. Checks to see if
                    it already exists, if it does not, creates it.
                    (Defaults to 'tor-cloud-servers')''')

parser.add_argument('--keypair', '-k', dest='keypair',
                    help='''Trys to use the keypair selected, if it does not
                    exist, creates it.  (Defaults to
                    ~/.ssh/tor-cloud-servers.pem)''')

parser.add_argument('--user-data', '-u', dest='user_data',
                    help='''Auto-run a script when the instance starts. 
                    (Default is None. You usually don't need to mess with
                    this)''', default=None)


bridge_type = parser.add_mutually_exclusive_group()
bridge_type.add_argument('--private', action='store_true',
                         dest='private', help='''Creates a Private Bridge.''')
bridge_type.add_argument('--normal',  action='store_true',
                         dest='normal', help='''Creates a Normal Bridge. (Default)''')


instance_type = parser.add_mutually_exclusive_group()
instance_type.add_argument('--micro', action='store_true', dest='micro',
                           help='''Instance Type: Micro (Default)''')
instance_type.add_argument('--small', action='store_true', dest='small',
                           help='''Instance Type: Small ''')
instance_type.add_argument('--hcpumedium', action='store_true', 
                           dest='highmed', help='''Instance Type:
                           High-CPU Medium''')
instance_type.add_argument('--medium', action='store_true', dest='med',
                           help='''Instance Type: Medium''')

ami = parser.add_mutually_exclusive_group()
ami.add_argument('--us-east-1',  action='store_true', dest='use1',
                 help='''Region: Virginia (Default)''')
ami.add_argument('--us-west-1',  action='store_true', dest='usw1',
                 help='''Region: North California''')
ami.add_argument('--us-west-2',  action='store_true', dest='usw2',
                 help='''Region: Oregon''')
ami.add_argument('--eu-west-1', action='store_true', dest='euw1',
                 help='''Region: Ireland''')
ami.add_argument('--ap-northeast-1', action='store_true', dest='apne1',
                 help='''Region: Tokyo''')
ami.add_argument('--ap-southeast-1', action='store_true', dest='apse1',
                 help='''Region: Singapore''')
ami.add_argument('--sa-east-1', action='store_true', dest='sae1',
                 help='''Region: Sao Paulo''')

Args = parser.parse_args()

