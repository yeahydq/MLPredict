# Setup Kubeflow

In this part, you will setup kubeflow on an existing kubernetes cluster.

## Requirements
* Aws account
* Docker and kubernetes (k8s) basic knowledge
* Machine Learning, Deep learning knowledge

# To setup local client [Reference](https://github.com/yeahydq/MLPipeline/blob/master/kubeflow_env_setup/README.md)

```bash
./kubeflow_env_setup/install_kops-official.sh
```

## End to End
```bash
cd /tmp/ && rm -rf MLPipeline
git clone https://github.com/yeahydq/MLPipeline.git
cd MLPipeline
#./kubeflow_env_setup/install_kops-official.sh
./kubeflow_env_setup/setupKubeflow.sh
```


```bash
cd ./argo/demo/
./createDockerMnist.sh
./createDockerMnist2.sh
./submitJob.sh
# https://github.com/kubeflow/examples/blob/master/github_issue_summarization/notebooks/train.py
```


# Create a docker
```bash
export GITHUB_TOKEN=4d14dc683ce1baa8d3eb94f3c3396091ba0d9c55

cd /tmp/MLPipeline/argo/ks/docker/
cd /tmp/MLPipeline/argo/ks/dockertest/

source activate tensorflow_p36
python ./mnist_estimator_datasetinput.py
```

```bash
./createDockerbenchmarks.sh
./createDocker.sh
./createDockerMnistbasic.sh
```


kubectl config set-context myfirstcluster13.k8s.local --namespace=kubeflow


# Create manifest
```bash
cd /tmp
rm -rf dist-mnist
#ks init dist-mnist --context kubeflow
ks init dist-mnist --context myfirstcluster13.k8s.local
cd dist-mnist
```

```bash
JOB_NAME=mycnnjob

ks registry add ks github.com/yeahydq/MLPipeline/tree/master/argo/ks
ks pkg install ks/tf-job

# alias of ks prototype use
ks generate tf-job ${JOB_NAME} --name=${JOB_NAME}
```

# Check YAML content
```bash
dockerName=mytfmnistbasic
IMAGE=757977731860.dkr.ecr.us-east-1.amazonaws.com/dy/${dockerName}
GPUIMAGE=757977731860.dkr.ecr.us-east-1.amazonaws.com/dy/${dockerName}gpu

ks param set ${JOB_NAME} image ${IMAGE}
ks param set ${JOB_NAME} image_gpu ${GPUIMAGE}
ks param set ${JOB_NAME} num_ps 1
ks param set ${JOB_NAME} num_workers 1
ks param set ${JOB_NAME} num_masters 0
ks param set ${JOB_NAME} num_chiefs 0
ks param set ${JOB_NAME} num_gpus 1        # per pod
ks param set ${JOB_NAME} args -- train_steps=200000
#ks param set ${JOB_NAME} args -- /usr/bin/python3,/opt/model.py
#ks param set ${JOB_NAME} args -- python,/app/mnist_estimator.py,--steps,1000


ks param set ${JOB_NAME} envs -- '[ {"name": "TF_MODEL_DIR", "value": "/models/mycnnjob2"},  {"name": "TF_MAX_TRAIN_STEPS", "value": "20000"},  {"name": "NUM_GPUS_PER_WORKER", "value": "1"},  {"name": "TF_STRATEGY", "value": "parameter_server_strategy"}]'

ks param set ${JOB_NAME} envs -- '[ {"name": "TF_MODEL_DIR", "value": "/models/mycnnjob3"},  {"name": "TF_MAX_TRAIN_STEPS", "value": "20000"},  {"name": "NUM_GPUS_PER_WORKER", "value": "1"},  {"name": "TF_STRATEGY", "value": "collective_all_reduce_strategy"}]'
```

```bash
ks show default
ks delete default -c ${JOB_NAME}
ks apply default -c ${JOB_NAME}
```

```bash
kubectl get tfjob
kubectl describe tfjob mycnnjob
kubectl describe pod mycnnjob-ps-0
kubectl describe pod mycnnjob-worker-0
kubectl describe pod mycnnjob-worker-1
keyWord=${JOB_NAME}
tfjobName=`kubectl get tfjob -n kubeflow | grep "$keyWord" | awk '{print $1}'`
```

```bash
kubectl logs ${tfjobName}-master-0 -n kubeflow -f
kubectl logs ${tfjobName}-worker-0 -n kubeflow -f
kubectl logs ${tfjobName}-worker-1 -n kubeflow -f
kubectl logs ${tfjobName}-worker-2 -n kubeflow -f
kubectl logs ${tfjobName}-ps-0 -n kubeflow -f

kubectl exec mycnnjob-worker-0  -n kubeflow  -it -- bash
kubectl exec mycnnjob-worker-1  -n kubeflow  -it -- bash

watch -n 2 nvidia-smi
```

https://github.com/kubeflow/tf-operator/tree/master/test/workflows/components


gpu: kops.k8s.io/instancegroup=gpunodes
cpu: kops.k8s.io/instancegroup=nodes

          nodeSelector:
            kops.k8s.io/instancegroup: gpunodes

# check log
```bash
argo list
argo get tf-workflow-bm7p7
kubectl describe pod tf-workflow-bm7p7-2898015436 -n kubeflow | tail
kubectl logs tf-workflow-wmpbx -n kubeflow -f
```

# delete
```bash
keyWord=myjob
argo list | grep workflow | awk '{print $1}' | xargs -n1 -i argo delete {}
kubectl get deployment --all-namespaces | grep "$keyWord" | awk '{print $2}' | xargs -n1 -i kubectl delete deployment {}
kubectl get tfjob | grep "$keyWord" | awk '{print $1}' | xargs -n1 -i kubectl delete tfjob {}
kubectl get service --all-namespaces | grep "$keyWord" | awk '{print $2}' | xargs -n1 -i kubectl delete service {}
kubectl get pod --all-namespaces | grep "$keyWord" | awk '{print $2}' | xargs -n1 -i kubectl delete pod {}

```

```bash
export NAME=myfirstcluster13.k8s.local
export KOPS_STATE_STORE=s3://dy-k8s-state-store
kops delete cluster --name myfirstcluster13.k8s.local --yes
```


https://github.com/kubernetes/kops/issues/4391

# Setup the tensorboard
```bash
nohup kubectl port-forward tensorboard-myjob-6967d-6d7685694d-mnjsz -n kubeflow 6006:6006 &

scp -i ~/keys/dick2EC2 ec2-user@35.171.45.50:/home/ec2-user/.kube/config ~/.kube/config
ssh -L 6006:localhost:6006 -i ~/keys/dick2EC2 ec2-user@35.171.45.50 -N &
http://localhost:6006/

```

# Other command for quick reference

```bash
cat <<EOF > /tmp/pod1.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod1
spec:
  containers:
  - name: shell
    image: 757977731860.dkr.ecr.us-east-1.amazonaws.com/dy/mytfmnistreplicagpu
    env:
    - name: TF_TRAIN_STEPS
      value: "20000"
    - name: TF_MAX_TRAIN_STEPS
      value: "20000"
    - name: NUM_GPUS_PER_WORKER
      value: "1"
    resources:
      limits:
        nvidia.com/gpu: 1 # requesting 1 GPU
EOF
cat <<EOF > /tmp/pod2.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod2
spec:
  containers:
  - name: shell
    image: 757977731860.dkr.ecr.us-east-1.amazonaws.com/dy/mytfmnistreplicagpu
    env:
    - name: TF_TRAIN_STEPS
      value: "20000"
    resources:
      limits:
        nvidia.com/gpu: 1 # requesting 1 GPU
EOF

kubectl delete -f /tmp/pod1.yaml
kubectl delete -f /tmp/pod2.yaml
kubectl apply -f /tmp/pod1.yaml
kubectl apply -f /tmp/pod2.yaml

kubectl describe pod pod1
kubectl logs pod1 -f

kubectl describe pod pod2
kubectl logs pod2 -f
sudo lsmod | grep br_netfilter




cat <<EOF > /tmp/pod1.yaml
---
apiVersion: kubeflow.org/v1beta1
kind: TFJob
metadata:
  labels:
    ksonnet.io/component: mycnnjob
  name: mycnnjob
  namespace: kubeflow
spec:
  tfReplicaSpecs:
    PS:
      replicas: 1
      template:
        spec:
          containers:
          - env:
            - name: TF_MODEL_DIR
              value: /models/mycnnjobx1
            - name: TF_MAX_TRAIN_STEPS
              value: "200000"
            - name: NUM_GPUS_PER_WORKER
              value: "1"
            - name: TF_STRATEGY
              value: "parameter_server_strategy"
            image: 757977731860.dkr.ecr.us-east-1.amazonaws.com/dy/mytfmnistreplica
            name: tensorflow
            ports:
            - containerPort: 2222
              name: tfjob-port
            volumeMounts:
            - mountPath: /models
              name: models
          restartPolicy: OnFailure
          volumes:
          - name: models
            persistentVolumeClaim:
              claimName: models
          nodeSelector:
            kops.k8s.io/instancegroup: nodes
    WORKER:
      replicas: 1
      template:
        spec:
          containers:
          - env:
            - name: TF_MODEL_DIR
              value: /models/mycnnjobx2
            - name: TF_MAX_TRAIN_STEPS
              value: "200000"
            - name: NUM_GPUS_PER_WORKER
              value: "1"
            - name: TF_STRATEGY
              value: "parameter_server_strategy"
            image: 757977731860.dkr.ecr.us-east-1.amazonaws.com/dy/mytfmnistreplicagpu
            name: tensorflow
            ports:
            - containerPort: 2222
              name: tfjob-port
            resources:
              limits:
                nvidia.com/gpu: 1
            volumeMounts:
            - mountPath: /models
              name: models
          restartPolicy: OnFailure
          volumes:
          - name: models
            persistentVolumeClaim:
              claimName: models
          nodeSelector:
            kops.k8s.io/instancegroup: gpunodes
EOF


kubectl delete -f  /tmp/pod1.yaml
kubectl apply -f  /tmp/pod1.yaml

kubectl logs pod1 -n kubeflow -f
```

# Other reference
```
https://github.com/kubeflow/tf-operator/blob/master/examples/distribution_strategy/distributed_tfjob.yaml
https://github.com/kubeflow/kubeflow/tree/master/kubeflow/openmpi
https://github.com/tensorflow/tensorflow/issues/6116
https://www.jianshu.com/p/937a0ce99f56
https://towardsdatascience.com/howto-profile-tensorflow-1a49fb18073d
```