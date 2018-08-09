import boto3
from dict_to_obj import Struct

class Ec2Manager():

    ec2Instances = []
    ec2 = None

    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def load_instances(self):
        ec2instances = Struct(self.ec2.describe_instances(
            Filters = [
                {'Name': 'tag:RestartShutdown', 'Values': ['yes']}
                #{'Name': 'tag:Name', 'Values': ['ELK_docker']}
            ]
        ))
        for reservation in ec2instances.Reservations:
            self.ec2Instances.extend(reservation.Instances)

    # EC2 status
    # 0 : pending
    # 16 : running
    # 32 : shutting-down
    # 48 : terminated
    # 64 : stopping
    # 80 : stopped

    # start == true -> starts the instance
    # start == false -> stops the instance
    def change_status_instances(self, start):
        if(self.ec2Instances == None):
            return

        statusFilter = 80 if start else 16
        instancesIds = []
        for instance in self.ec2Instances:
            if(instance.State.Code == statusFilter):
                instancesIds.append(instance.InstanceId)

        if(start):
            response = self.ec2.start_instances( InstanceIds= instancesIds )
        else:
            response = self.ec2.stop_instances( InstanceIds= instancesIds )

        print(response)

