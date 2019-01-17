# HDP ANSIBLE API - HIVE LLAP

This Projects aims at installing [HIVE LLAP](https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.6.5/bk_command-line-installation/content/install_hive_llap.html) using ambari's API.
You can have already one instance running on your cluster, it will isolate new instances.
You can place new instance whatever the node ( of course avoid edge nodes).

SLIDER, HDFS, HIVE, YARN, MAPREDUCE2, ZOOKEEPER services must be already installed on the cluster.
This scripts will just add `HIVE_SERVER_INTERACTIVE` component to `HIVE` service.

You can install the cluster using [hdp-ansible-api project for example](https://github.com/yyounes75/hdp-ansible-api).

It:
* copy ambari server/agent scripts
* Copy the keytabs if necessary
* create service/component configuration through API
* add config groups through API

## Steps to install HIVE LLAP (done by playbook)

- Install CLIENTS:
 * HDFS_CLIENT
 * YARN_CLIENT
 * HIVE_CLIENT
 * PIG
 * TEZ_CLIENT
 * SLIDER_CLIENT

- Add  Zookeeper url configuration for hive Server 2 Interactive unless
you have already one instance of hive llap running on your cluster.

- Add configuration groups
each instance will have its own LLAP configuration 5 daemon size, cache, executors numbers...)

- Install Hive Service Interactive:
Do Ambari Put request to install effectively the hive Server component on the host.

- Duplicate the keytab from `hive.service.keytab` to `hive.llap.zk.sm.keytab` so slider manager
can authenticate toward zookeeper.

It DOES NOT start HiveServerInteractive Service.
You have to do it manually

## Example

This is an extract of an ansible deploy file
```yaml
############### HIVE LLAP ##########

- hosts: "{{ ambari_server }}"
  gather_facts: no
  vars_files:
  - vars/external_vars_dev.yml

  roles:
    - role: hdp-ansible-ambari-llap
      tags: ambari_hive_llap
      vars:
        ambari_server_hostname: '{{ ambari_server }}'
        ambari_server_port: '{{ ambari_server_ssl_port }}'
        ambari_server_protocol: https
        ambari_namespace: dev
        cluster_name: dev
        ambari_username: admin
        ambari_password: admin
        zk_url: master01.metal.ryba:2181,master02.metal.ryba:2181,master03.metal.ryba:2181
        llap_configs:
          - host: master01.metal.ryba
            config:
              hive-interactive-site:
                - hive.llap.daemon.queue.name=default #Yarn Queue Name
                - hive.server2.tez.default.queues=default
                - hive.server2.zookeeper.namespace=hiveserver2-llapmaster01 # zooKeeperNamespace
                - hive.llap.daemon.service.hosts=@llapmaster01
                - hive.server2.tez.sessions.per.default.queue=1
                - hive.llap.daemon.yarn.container.mb=1024 # (Memory per Daemon)
                - hive.llap.io.memory.size=256
                - hive.llap.daemon.num.executors=1 # num of executors
                - hive.llap.io.threadpool.size=1
              tez-interactive-site:
                - tez.am.resource.memory.mb=512
              tez-interactive-env: []
              hive-interactive-env:
                - hive_heapsize=512 # Heap Size of HiveServer2 Interactive
                - llap_app_name=llapmaster01 #LLAP Instance Name
                - slider_am_container_mb=512
                - llap_heap_size=256 #(LLAP Daemon Heap Size)
          - host: master02.metal.ryba
            config:
              hive-interactive-site:
                - hive.llap.daemon.queue.name=default #Yarn Queue Namehayasta6
                - hive.server2.tez.default.queues=default
                - hive.server2.zookeeper.namespace=hiveserver2-llapmaster02 # zooKeeperNamespace
                - hive.llap.daemon.service.hosts=@llapmaster02
                - hive.server2.tez.sessions.per.default.queue=1
                - hive.llap.daemon.yarn.container.mb=1024 # (Memory per Daemon)
                - hive.llap.io.memory.size=256
                - hive.llap.daemon.num.executors=1 # num of executors
                - hive.llap.io.threadpool.size=1
              tez-interactive-site:
                - tez.am.resource.memory.mb=512
              tez-interactive-env: []
              hive-interactive-env:
                - hive_heapsize=512 # Heap Size of HiveServer2 Interactive
                - llap_app_name=llapmaster02 #LLAP Instance Name
                - slider_am_container_mb=512
                - llap_heap_size=256 #(LLAP Daemon Heap Size)
```
