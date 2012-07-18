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
from os import path
import sys

import boto
import requests

from args import Args

###
#   Functions
###
def launch_instance(ec2,
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
    familiar to anyone who has read 'Python and AWS' by Mitch Garnatt.
    '''
    try:
        key = ec2.get_all_key_pairs(keynames=[key_name])[0]
    except ec2.ResponseError, e:
        if e.code == 'InvalidKeyPair.NotFound' :
            print 'Creating keypair: %s' % key_name
            key = ec2.create_key_pair(key_name)
            key.save(key_dir)
        else:
            raise

    try:
        group = ec2.get_all_security_groups(groupnames=[group_name])[0]
    except ec2.ResponseError, e:
        if e.code == 'InvalidGroup.NotFound':
            print 'Creating Security Group: %s' % group_name
            group = ec2.create_security_group(group_name,
                                              'Security Group for Tor Nodes')
        else:
            raise

    try:
        group.authorize('https', ssh_port, ssh_port, cidr)
    except ec2.ResponseError, e:
        if e.code == 'InvalidPermission.Duplicate':
            print 'Security Group: %s already authorized' % group_name
        else:
            raise

    reservation = ec2.run_instances(ami,
                                    key_name=key_name,
                                    security_groups=[group_name],
                                    instance_type=instance_type,
                                    user_data=user_data)
    instance = reservation.instances[0]

    while instance.state != 'running' :
        print '.'
        time.sleep(5)
        instance.update()

    return instance

def get_ami(Args):
    '''
    Gets the correct AMI.
    '''
    if Args.private:
        if Args.use1:
            return 'ami-8467bfed'
        elif Args.usw1:
            return 'ami-63207b26'
        elif Args.usw2:
            return 'ami-baf27e8a'
        elif Args.euw1:
            return 'ami-f5390281'
        elif Args.apne1:
            return 'ami-78e05079'
        elif Args.apse1:
            return 'ami-e63472b4'
        elif Args.sae1:
            return 'ami-c4a07ed9'
        else:
            return 'ami-8467bfed'
    elif Args.normal:
        if Args.use1:
            return 'ami-4e6eb627'
        elif Args.usw1:
            return 'ami-892378cc'
        elif Args.usw2:
            return 'ami-24f27e14'
        elif Args.euw1:
            return 'ami-6d447f19'
        elif Args.apne1:
            return 'ami-78ff4f79'
        elif Args.apse1:
            return 'ami-e45016b6'
        elif Args.sae1:
            return 'ami-b4a07ea9'
        else:
            return 'ami-4e6eb627'
    else:
        return 'ami-4e6eb627'
    

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


if __name__ == '__main__':
    try:
        ec2 = boto.connect_ec2()
    except boto.exception.NoAuthHandlerFound:    
        pass
    try:
        ec2 = boto.connect_ec2(Args.akid, Args.sak)
    except:
        sys.exit(1)

    instance_type = get_type(Args)
    ami = get_ami(Args)

    instance = launch_instance(ec2=ec2, 
                               instance_type=instance_type,
                               ami=ami)
    if instance:
        print "Your " + instance.instance_type + " instance is running!"
        print "IP:", instance.ip_address
        print "ID:", instance.id
        print "Region:", instance.region
        print "DNS name:", instance.dns_name
