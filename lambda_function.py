from emr_manager import EmrManager
from rds_manager import RdsManager
from ec2_manager import Ec2Manager


def lambda_handler(event, context):
    startInstances = (event['action'] == 'start')

    print('action: ' + event['action'])

    print('EC2')
    ec2Manager = Ec2Manager()
    ec2Manager.load_instances()
    ec2Manager.change_status_instances(startInstances)

    print('RDS')
    rdsManager = RdsManager()
    rdsManager.load_db_instances()
    rdsManager.change_status_instances(startInstances)
