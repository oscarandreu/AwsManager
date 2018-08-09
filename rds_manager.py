import boto3
from dict_to_obj import Struct

class RdsManager():

    rdsInstances = []
    rds = None

    def __init__(self):
        self.rds = boto3.client('rds')

    def check_shutdown_tag(self, instance):
        tags = Struct(self.rds.list_tags_for_resource(ResourceName= instance.DBInstanceArn))
        for tag in tags.TagList:
            if(tag.Key == 'RestartShutdown' and tag.Value == 'yes'):
                return True
        return False

    def load_db_instances(self):
        rdsinstances = Struct(self.rds.describe_db_instances())
        for instance in rdsinstances.DBInstances:
            if(self.check_shutdown_tag(instance)):
                self.rdsInstances.append(instance)

    # start == true -> starts the instance
    # start == false -> stops the instance
    def change_status_instances(self, start):
        if(self.rdsInstances == None):
            return

        statusFilter = 'stopped' if start else 'available'
        for instance in self.rdsInstances:
            if(instance.DBInstanceStatus == statusFilter):
                if(start):
                    response = self.rds.start_db_instance( DBInstanceIdentifier= instance.DBInstanceIdentifier )
                else:
                    response = self.rds.stop_db_instance( DBInstanceIdentifier= instance.DBInstanceIdentifier )
                print(response)