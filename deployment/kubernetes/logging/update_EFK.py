#!/usr/bin/python3

import os
import sys
sys.path.append(sys.argv[1])
sys.path.append(sys.argv[1] + "../")
import yaml_utils

#kibana
yaml_file = sys.argv[1] + "kibana-deploy.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
data["spec"]["template"]["spec"]["volumes"][1]["hostPath"]["path"] = sys.argv[1] + "config"
yaml_utils.dump_yaml_file(data, yaml_file)
