Lab 4.1: Eviction
=================

This lab deals with out of resource handling on OpenShift platforms, most importantly the handling of out-of-memory and disk full conditions. Out of resource conditions can occur either on the container level because of resource limits or on the node level because a node runs out of memory or disk space.
They are either handled by OpenShift or directly by the kernel.

Lab 4.1.1: Container oom
------------------------

Create a container which allocates memory till it's being killed.

    oc new-project lab41
    oc new-app https://github.com/appuio/ops-techlab/blob/master/resources/membomb.yaml

Wait till the container is up and being killed. `oc get pods -o wide` will then show:

    NAME              READY     STATUS    RESTARTS   AGE       IP            NODE
    membomb-1-h2b1q   0/1       Error     0          14s       10.130.0.16   ose3-node2.example.com

After the container is being killed more than once status switches to `CrashLoopBackOff`.
Run `oc describe pod -l app=membomb` to get more information about the container state which should look like this:

    Last State:         Terminated
      Reason:           Error
      Exit Code:        137
      Started:          Tue, 20 Mar 2018 18:59:49 +0100
      Finished:         Tue, 20 Mar 2018 18:59:54 +0100

Exit code 137 [indicates](http://tldp.org/LDP/abs/html/exitcodes.html) that the container main process was kill by the `SIGKILL` signal.

Scale down the container to stop the memory bomb:

    oc scale dc membomb --replicas=0

To determine the cause for the `SIGKILL` signal SSH into the machine on which the pod ran and check the system logs around the termination time using `journalctl`. You should find something like:

    Mar 20 18:59:53 ose3-node2.example.com kernel: Out of memory: Kill process 14675 (membomb) score 1831 or sacrifice child
    Mar 20 18:59:53 ose3-node2.example.com kernel: Killed process 14675 (membomb) total-vm:3223664kB, anon-rss:3222912kB, file-rss:0kB, shmem-rss:0kB

Endangers system stability
Heuristic

not confuse resources with deployer


    NAME              READY     STATUS      RESTARTS   AGE
    membomb-3-hftq5   0/1       OOMKilled   0          7s

Again run `oc describe pod -l app=membomb` to get more information about the container state which should look like this:

    Last State:         Terminated
      Reason:           OOMKilled
      Exit Code:        137
      Started:          Wed, 21 Mar 2018 16:52:18 +0100
      Finished:         Wed, 21 Mar 2018 16:52:18 +0100


    Mar 21 16:52:13 ose3-node1.example.com kernel: Memory cgroup out of memory: Kill process 13801 (membomb) score 1730 or sacrifice child
    Mar 21 16:52:13 ose3-node1.example.com kernel: Killed process 13801 (membomb) total-vm:1048224kB, anon-rss:1047400kB, file-rss:0kB, shmem-rss:0kB

Affects this container only. Pod and any other containers it contains live on.
