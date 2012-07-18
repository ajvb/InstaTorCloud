import argparse


parser = argparse.ArgumentParser(description='''InstaTorCloud -- Get a
                                     Tor Bridge running on an EC2 instance in
                                     a single command.''')

parser.add_argument('-v', '--version', action='version',
                     version='InstaTorCloud v0.1')

parser.add_argument('--access-key-id', '-akid', action='store', dest='akid',
                    help='''Where you must insert your AWS Access Key ID.
                    (More info here: http://goo.gl/fCVGi)''',
                    required=True)
parser.add_argument('--secret-access-key', '-sak', action='store', dest='sak',
                    help='''Where you must insert your AWS Secret Access Key.
                    (More info here: http://goo.gl/fCVGi)''',
                    required=True)

parser.add_argument('--security-group', '-secgrp', action='store',
                    dest='secgrp', help='''Name of the Security Group
                    you want to use for the instance. Checks to see if
                    it already exists, if it does not, creates it.
                    (Defaults to 'tor-cloud-servers')
                    ''')

parser.add_argument('--keypair', '-kp', action='store', dest='keypair',
                    help='''Trys to use the keypair selected, if it does not
                    exist, creates it.  (Defaults to ~/.ssh/tor-cloud-servers.pem
                    if nothing is inputted.)''')

parser.add_argument('--user-data', '-ud', action='store', dest='userdata',
                    help='''Auto-run a script when the instance starts. 
                    (Default is None. You usually don't need to mess with
                    this)''')


bridge_type = parser.add_mutually_exclusive_group()
bridge_type.add_argument('--private', '-prvt', action='store_true',
                         dest='private', help='''Creates a Private Bridge.''')
bridge_type.add_argument('--normal', '-nrml', action='store_true',
                         dest='normal', help='''Creates a Normal Bridge. (Default)''')


instance_type = parser.add_mutually_exclusive_group()
instance_type.add_argument('--micro', action='store_true', dest='micro',
                           help='''Micro Instance Type. (Default)''')
instance_type.add_argument('--small', action='store_true', dest='small',
                           help='''Small Instance Type.''')
instance_type.add_argument('--hcpumedium', action='store_true', 
                           dest='highmed', help='''High-CPU Medium Instance
                           Type.''')
instance_type.add_argument('--medium', action='store_true', dest='med',
                           help='''Medium Instance Type.''')

ami = parser.add_mutually_exclusive_group()
ami.add_argument('--us-east-1', '-use1', action='store_true', dest='use1',
                 help='''Virginia (Default)''')
ami.add_argument('--us-west-1', '-usw1', action='store_true', dest='usw1',
                 help='''North California''')
ami.add_argument('--us-west-2', '-usw2', action='store_true', dest='usw2',
                 help='''Oregon''')
ami.add_argument('--eu-west-1', '-euw1', action='store_true', dest='euw1',
                 help='''Ireland''')
ami.add_argument('--ap-northeast-1', '-apne1', action='store_true', dest='apne1',
                 help='''Tokyo''')
ami.add_argument('--ap-southeast-1', '-apse1', action='store_true', dest='apse1',
                 help='''Singapore''')
ami.add_argument('--sa-east-1', '-sae1', action='store_true', dest='sae1',
                 help='''Sao Paulo''')

Args = parser.parse_args()

