#   InstaTorCloud
#   Orginal Author: AJ Bahnken / aj@ajvb.me
#   Maintained by The Cloak Project / thecloakproject.org
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>

import argparse
import time
import os
import sys

import boto

from args import Args

###
#   Functions.
###
def launch_bridge(ec2,
                  instance_type,
                  ami,
                  group_name='tor-cloud-servers',
                  key_name='tor-cloud-servers',
                  key_extension='.pem',
                  key_dir='~/.ssh',
                  ssh_port=22,
                  cidr='0.0.0.0/0',
                  user_data=None,
                  ssh_passwd=None):
    '''
    The main function of this application. Will look extremely
    familiar to anyone who has read 'Python and AWS' by Mitch Garnaat.
    '''
    try:
        key = ec2.get_all_key_pairs(keynames=[key_name])[0]
        print 'Found keypair: %s' % key_name
    except ec2.ResponseError, e:
        if e.code == 'InvalidKeyPair.NotFound' :
            print 'Creating keypair: ', key_name
            key = ec2.create_key_pair(key_name)
            key.save(key_dir)
        else:
            raise

    try:
        group = ec2.get_all_security_groups(groupnames=[group_name])[0]
        print 'Found Security Group: ', group_name
    except ec2.ResponseError, e:
        if e.code == 'InvalidGroup.NotFound':
            print 'Creating Security Group: ', group_name
            group = ec2.create_security_group(group_name,
                                              'Security Group for Tor Nodes')
        else:
            raise

    try:
        group.authorize('tcp', ssh_port, ssh_port, cidr)
        print 'Authorized SSH'
    except ec2.ResponseError, e:
        if e.code == 'InvalidPermission.Duplicate':
            print group_name, ' already has a SSH rule.'
        else:
            raise

    try:
        group.authorize('tcp', 443, 443, cidr)
        print 'Authorized HTTPS'
    except ec2.ResponseError, e:
        if e.code == 'InvalidPermission.Duplicate':
            print group_name, ' already has a HTTPS rule.'
    
    try:
        group.authorize('tcp', 40872, 40872, cidr)
        print 'Authorized 40872'
    except ec2.ResponseError, e:
        if e.code == 'InvalidPermission.Duplicate':
            print group_name, ' already has a 40872 rule.'
    
    try:
        group.authorize('tcp', 52176, 52176, cidr)
        print 'Authorized 52176'
    except ec2.ResponseError, e:
        if e.code == 'InvalidPermission.Duplicate':
            print group_name, ' already has a 52176 rule.'

    reservation = ec2.run_instances(ami,
                                    key_name=key_name,
                                    security_groups=[group_name],
                                    instance_type=instance_type,
                                    user_data=user_data)
    instance = reservation.instances[0]

    print 'Starting instances'
    while instance.state != 'running' :
        print 'waiting...'
        time.sleep(5)
        instance.update()

    return instance

def get_ami(Args):
    '''
    Gets the correct AMI.
    '''
    if Args.private:
        if Args.use1:
            return 'ami-567c1a3f'
        elif Args.usw1:
            return 'ami-1aecc05f'
        elif Args.usw2:
            return 'ami-d29403e2'
        elif Args.euw1:
            return 'ami-22011556'
        elif Args.apne1:
            return 'ami-0a1c9e0b'
        elif Args.apse1:
            return 'ami-601c5332'
        elif Args.sae1:
            return 'ami-6bd30976'
        elif Args.apse2:
            return 'ami-0e920234'
        else:
            return 'ami-567c1a3f'
    elif Args.normal:
        if Args.use1:
            return 'ami-4a7c1a23'
        elif Args.usw1:
            return 'ami-18ecc05d'
        elif Args.usw2:
            return 'ami-d09403e0'
        elif Args.euw1:
            return 'ami-20011554'
        elif Args.apne1:
            return 'ami-061c9e07'
        elif Args.apse1:
            return 'ami-621c5330'
        elif Args.sae1:
            return 'ami-69d30974'
        elif Args.apse2:
            return 'ami-08920232'
        else:
            return 'ami-4a7c1a23'
    else:
        return 'ami-4a7c1a23'

def get_type(Args):
    '''
    Gets the Instance Type through checking out the Args.
    '''
    if Args.small:
        return 'm1.small'
    elif Args.highmed:
        return 'c1.medium'
    elif Args.med:
        return 'm1.medium'
    else:
        return 't1.micro'


      ############
      ### Main ###
      ############
if __name__ == '__main__':
    try:
        try:
            ec2 = boto.connect_ec2()
        except:
            ec2 = boto.connect_ec2(Args.akid, Args.sak)
        ec2.get_all_instances()
    except:
        print "\nUnable to connect to EC2 using your AWS keys."
        print "Double check them. If you need some help check out:"
        print "http://docs.amazonwebservices.com/AWSSecurityCredentials/1.0/AboutAWSCredentials.html#AccessKeys"
        print "or"
        print "http://goo.gl/fCVGi\n"
        sys.exit(1)

    instance_type = get_type(Args)
    ami = get_ami(Args)

    if Args.keypair:
        thekey = os.path.split(Args.keypair)
        keydir = thekey[0]
        keyname = thekey[1].split('.')[0]
        keyextension = '.' + thekey[1].split('.')[-1]
    else:
        keyname = 'tor-cloud-servers'
        keyextension = '.pem'
        keydir = '~/.ssh'


    if Args.secgrp:
        secgrp = Args.secgrp
    else:
        secgrp = 'tor-cloud-servers'
    instance = launch_bridge(ec2=ec2,
                             instance_type=instance_type,
                             ami=ami,
                             group_name=secgrp,
                             key_name=keyname,
                             key_extension=keyextension,
                             key_dir=keydir,
                             user_data=Args.user_data)
    if instance:
        print "Your ", instance.instance_type, " instance is running!"
        print "IP: ", instance.ip_address
        print "ID: ", instance.id
        print "Region: ", instance.region
        print "DNS name: ", instance.dns_name
    else:
        print "something went horribly wrong....."
        sys.exit(1)
