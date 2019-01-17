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
