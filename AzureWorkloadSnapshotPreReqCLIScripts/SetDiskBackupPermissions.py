#
# Copyright 2021 (c) Microsoft Corporation
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this script and associated documentation files (the "script"), to deal
# in the script without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the scipt, and to permit persons to whom the script is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the script.

# THE SCRIPT IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SCRIPT OR THE USE OR OTHER DEALINGS IN THE
# SCRIPT

import os
import fileinput
import sys
import argparse
import time
from helpers import *

#Enabling colors in the command prompt
os.system("color")

desc = bcolors.OKBLUE + "This script will assign the required roles for the backup vault msi on the respective disk and snapshot resource groups for Azure disk backup. \n \n Assigns Disk Backup Reader on the resource group which has disks. \n Assigns Disk Snapshot Contributor on the resource group where disk snapshots will be created." + bcolors.ENDC

parser = argparse.ArgumentParser(description=desc)

requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("--subscription", "-s", help="Subscription Id for disk resource groups and the snapshot resource group", required=True)
requiredNamed.add_argument("--msi", "-v", help="Resource group for the virtual machine containing workload", required=True)
requiredNamed.add_argument("--disk-resource-groups", "-d", nargs='+', help="Resource group which contains the data disks", required=True)
requiredNamed.add_argument("--snapshot-resource-group", "-n", help="Target resource group for disk snapshots", required=True)

args = parser.parse_args()
subscription = args.subscription
msi = args.msi
disk_resource_groups = args.disk_resource_groups
snapshot_resource_group = args.snapshot_resource_group

diskBackupReaderRoleName = "Disk Backup Reader"
diskSnapshotContributorRoleName = "Disk Snapshot Contributor"

output = os.system("az login -o tsv --only-show-errors > login.txt")
output = os.system("az account set -s {} -o tsv --only-show-errors > context.txt".format(subscription))

if output == 0:
    print(bcolors.OKGREEN + "Successfully logged in to subscription " + subscription + "." + bcolors.ENDC)
    pass
else:
    print(bcolors.FAIL + "Script failed with unexpected error ... " + bcolors.ENDC)
    sys.exit()

print(bcolors.OKGREEN + "Assigning permissions to " + msi + bcolors.ENDC)

# Assign permissions for disk resource groups
for disk_resource_group in disk_resource_groups:
    assignRoleOnResourceGroup(msi, disk_resource_group, diskBackupReaderRoleName)        

# Assign permissions for snapshot resource groups to VM Identity
assignRoleOnResourceGroup(msi, snapshot_resource_group, diskSnapshotContributorRoleName)

print(bcolors.OKGREEN + "Script Execution completed" + bcolors.ENDC)