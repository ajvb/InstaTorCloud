#InstaTorCloud
#### Launch a Tor Bridge running on an EC2 instance in a single command.

To run with the defaults,

    python instatorcloud.py --access-key-id <ACCESS-KEY-ID> --secret-access-key <SECRET-ACCESS-KEY>

is all that is necessary.

This will great a Normal Bridge on a t1.micro instance type in the east-1 (Virginia) region, and will create (or use) a keypair and security-group, both called _'tor-cloud-server'_.

---------

If you change the security group or the keypair to use, InstaTorCloud will check to see if it exists, and if it does not, it will create it for you.

    python instatorcloud.py --access-key-id <ACCESS-KEY-ID> --secret-access-key <SECRET-ACCESS-KEY> 
    --security-group mytorbridges --keypair ~/.ssh/mytorbridges

You can also change what region your bridge will be in, whether it will be a private or a normal bridge, and what instance type it will be on..

    python instatorcloud.py --access-key-id <ACCESS-KEY-ID> --secret-access-key <SECRET-ACCESS-KEY> 
    --eu-west-1 --private --medium

And if you want, you can add it all together and even throw in a script to run once the instance has started. (Refered to as 'user_data'

    python instatorcloud.py --access-key-id <ACCESS-KEY-ID> --secret-access-key <SECRET-ACCESS-KEY> 
    --security-group mytorbridges --keypair ~/.ssh/mytorbridges --eu-west-1 --private --medium 
    --user-date myscript.sh

In full, the above command will create a Private bridge on a m1.medium instance type in the eu-west-1 (Ireland) region, use (or create) a key pair called _mytorbridges_ in ~/.ssh, use (or create) a security group called _mytorbridges_, and run a shell script called _myscript.sh_ once the instance has been successfully launched.

