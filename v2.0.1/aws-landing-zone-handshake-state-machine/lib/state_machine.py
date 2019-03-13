######################################################################################################################
#  Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           #
#                                                                                                                    #
#  Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance        #
#  with the License. A copy of the License is located at                                                             #
#                                                                                                                    #
#      http://aws.amazon.com/asl/                                                                                    #
#                                                                                                                    #
#  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES #
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    #
#  and limitations under the License.                                                                                #
######################################################################################################################

#!/bin/python

import boto3
import json
import inspect

class StateMachine(object):
    def __init__(self, logger):
        self.logger = logger
        self.state_machine_client = boto3.client('stepfunctions')
        
    def trigger_state_machine(self, state_machine_arn, input, name):
        try:
            self.logger.info("Starting execution of state machine: {} with input: {}".format(state_machine_arn, input))
            response = self.state_machine_client.start_execution(
                stateMachineArn=state_machine_arn,
                input=json.dumps(input),
                name=name
            )
            self.logger.info("State machine Execution ARN: {}".format(response['executionArn']))
            return response.get('executionArn')
        except Exception as e:
            message = {'FILE': __file__.split('/')[-1], 'METHOD': inspect.stack()[0][3], 'EXCEPTION': str(e)}
            self.logger.exception(message)
            raise
        
    def check_state_machine_status(self, execution_arn):
        try:
            self.logger.info("Checking execution of state machine: {}".format(execution_arn))
            response = self.state_machine_client.describe_execution(
                executionArn=execution_arn
            )
            self.logger.info("State machine Execution Status: {}".format(response['status']))
            if response['status'] == 'RUNNING':
                return 'RUNNING'
            elif response['status'] == 'SUCCEEDED':
                return 'SUCCEEDED'
            else:
                return 'FAILED'
        except Exception as e:
            message = {'FILE': __file__.split('/')[-1], 'METHOD': inspect.stack()[0][3], 'EXCEPTION': str(e)}
            self.logger.exception(message)
            raise        