Lab 3.2: Install Openshift Container Platform
============

Lab 3.2.2:  Install Openshift
-------------
## Installation of Openshift
In the previous lab we prepared the Ansible inventory to fit our test lab environment. Now we can prepare and run the installation.

Now we run the pre-install.yml playbook. This will do the following:
- Enable Ansible ssh pipelining.
- Attach all needed repositories for the installation of Openshift on all nodes
- Install the prerequisite packages: wget git net-tools bind-utils iptables-services bridge-utils bash-completion kexec-tools sos psacct
- Enable iptables on all nodes 
```
[ec2-user@master1 ~]$ ansible-playbook /home/ec2-user/resource/pre-install.yml
```

Run the installation in three steps. 
1. Installation of Openshift
```
[ec2-user@master1 ~]$ ansible-playbook /usr/share/ansible/openshift-ansible/playbooks/byo/config.yml
```
2. Deploying Openshift metrics
```
[ec2-user@master1 ~]$ ansible-playbook /usr/share/ansible/openshift-ansible/playbooks/byo/openshift-cluster/openshift-metrics.yml

```
3. Deploying Openshift logging
```
[ec2-user@master1 ~]$ ansible-playbook /usr/share/ansible/openshift-ansible/playbooks/byo/openshift-cluster/openshift-logging.yml
```

4. Add the cluster-admin role to the "shushu" user.
```
[ec2-user@master1 ~]$ oc adm policy --as system:admin add-cluster-role-to-user cluster-admin shushu
```

5. Now open your browser and access the master API with the user "shushu". Password is documented in the Ansible inventory.
```
https://master.user[X].lab.openshift.ch:8443/console/
```

## Verify Openshift installation
After the completion of the installation, we can verify, if everything is running as expected. Most of the checks are already been done by the playbooks.
First check if the API reachable and all nodes are ready with the right tags.
```
[ec2-user@master1 ~]$ oc get nodes --show-labels
```

Check if all pods are running and if Openshift could deploy all needed components
```
[ec2-user@master1 ~]$ oc get pods --all-namespaces
```

Check if all pvc are bound and glusterfs runs fine
```
[ec2-user@master1 ~]$ oc get pvc --all-namespaces
```

Check the etcd health status. This example is for "user1", you have to change it accordingly
```
[root@master1 ~]# etcdctl -C https://master1.[user].lab.openshift.ch:2379 --ca-file=/etc/origin/master/master.etcd-ca.crt --cert-file=/etc/origin/master/master.etcd-client.crt --key-file=/etc/origin/master/master.etcd-client.key cluster-health
member 92c764a37c90869 is healthy: got healthy result from https://172.31.46.235:2379
cluster is healthy

[root@master1 ~]# etcdctl -C https://master1.[user].lab.openshift.ch:2379 --ca-file=/etc/origin/master/master.etcd-ca.crt --cert-file=/etc/origin/master/master.etcd-client.crt --key-file=/etc/origin/master/master.etcd-client.key member list
92c764a37c90869: name=master1.user6.lab.openshift.ch peerURLs=https://172.31.46.235:2380 clientURLs=https://172.31.46.235:2379 isLeader=true
```

Create a project, run a build, push/pull from the internal registry and deploy a test application.
```
[ec2-user@master1 ~]$ oc new-project test
[ec2-user@master1 ~]$ oc new-app centos/ruby-22-centos7~https://github.com/openshift/ruby-ex.git
[ec2-user@master1 ~]$ oc get pods -w
[ec2-user@master1 ~]$ oc delete project test
```