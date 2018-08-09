from emr_manager import EmrManager
from rds_manager import RdsManager
from ec2_manager import Ec2Manager


if __name__ == "__main__":
    startInstances = True

    # ec2Manager = Ec2Manager()
    # ec2Manager.load_instances()
    # ec2Manager.change_status_instances(startInstances)

    # rdsManager = RdsManager()
    # rdsManager.load_db_instances()
    # rdsManager.change_status_instances(startInstances)

    emrManager = EmrManager()
    emrManager.load_clusters()    