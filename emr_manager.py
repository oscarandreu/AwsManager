import boto3
from dict_to_obj import Struct

class EmrManager():

    emrClusters = []
    emr = None

    def __init__(self):
        self.emr = boto3.client('emr')

    def load_clusters(self):
        emrinstances = Struct(self.emr.list_clusters(
            ClusterStates=[
                'RUNNING', 'WAITING'
            ]
        ))
        for cluster in emrinstances.Clusters:
            self.emrClusters.append(cluster.Id)
            print(cluster.Id)

    def disable_tables(self):
        for jobFlowId in self.emrClusters:
            response = self.emr.add_job_flow_steps(
                JobFlowId= jobFlowId,
                Steps = [
                    {
                        'Name': 'Disable all tables',
                        'ActionOnFailure': 'CANCEL_AND_WAIT',
                        'HadoopJarStep': {
                            'Jar': 'command-runner.jar',
                            'Args': [
                                '"/bin/bash","/usr/lib/hbase/bin/disable_all_tables.sh"',
                            ]
                        }
                    }
                ]
            )
            print(response)

    def stop_clusters(self):
        response = self.emr.terminate_job_flows(
            JobFlowIds = self.emrClusters
            )
        print(response)