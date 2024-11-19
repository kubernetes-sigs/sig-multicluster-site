# Configuring CoreDNS with the multicluster option

There is a ready made [CoreDNS multicluster plugin](https://coredns.io/explugins/multicluster/) you can use as the DNS component against MCS API implementations using EndpointSlices. By default, [CoreDNS](https://coredns.io/) does not include this plugin and it is therefore necessary to recompile CoreDNS to build a container image enabling this functionality.
The following paragraphs highlight how one can re-deploy CoreDNS with the [multicluster plugin](https://coredns.io/explugins/multicluster/). To illustrate the concepts, it has been chosen to use a Kind cluster with its default configuration.

## Step 1: Deploying a Kind cluster and checking its CoreDNS configuration

Kind provides an easy way to deploy a small cluster locally on your computer. To do so, you only need to deploy the kind CLI, and type:

```
kind create cluster --name cluster-1
```

**Output (Do Not Copy)**
```
Creating cluster "cluster-1" ...
 ✓ Ensuring node image (kindest/node:v1.25.3) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-cluster-1"
You can now use your cluster with:

kubectl cluster-info --context kind-cluster-1

Not sure what to do next? 😅  Check out https://kind.sigs.k8s.io/docs/user/quick-start/
```

You can then verify that CoreDNS is indeed well deployed:

```
kubectl get pods -n kube-system | grep coredns
```
**Output (Do Not Copy)**
```
coredns-565d847f94-brvlb                          1/1     Running   0          5m20s
coredns-565d847f94-zzdrd                          1/1     Running   0          5m20s
```

Before proceding with the re-compilation of CoreDNS, let's retrieve its current configuration by executing the command `coredns -plugins` in one of those pods.

```
kubectl exec -ti coredns-565d847f94-brvlb -n kube-system -- /coredns -plugins
```
**Output (Do Not Copy)**
```
Server types:
  dns

Caddyfile loaders:
  flag
  default

Other plugins:
  dns.acl
  dns.any
  dns.auto
  dns.autopath
  dns.azure
  dns.bind
  dns.bufsize
  dns.cache
  dns.cancel
  dns.chaos
  dns.clouddns
  dns.debug
  dns.dns64
  dns.dnssec
  dns.dnstap
  dns.erratic
  dns.errors
  dns.etcd
  dns.file
  dns.forward
  dns.geoip
  dns.grpc
  dns.header
  dns.health
  dns.hosts
  dns.k8s_external
  dns.kubernetes
  dns.loadbalance
  dns.local
  dns.log
  dns.loop
  dns.metadata
  dns.minimal
  dns.nsid
  dns.pprof
  dns.prometheus
  dns.ready
  dns.reload
  dns.rewrite
  dns.root
  dns.route53
  dns.secondary
  dns.sign
  dns.template
  dns.tls
  dns.trace
  dns.transfer
  dns.whoami
  on
```

This list is important as we will use it and just add the multicluster plugin to recompile CoreDNS.

## Re-compiling CoreDNS
The easiest way to recompile CoreDNS and generate a new container image is to use the instructions on the [official CoreDNS source repository](https://github.com/coredns/coredns#compilation-from-source). We specifically recommend the compilation with Docker which includes a ready-to-use Go environment.

Prior to triggering the compilation, it is necessary to modify the `plugin.cfg` file. First, it is highly recommended to keep the same plugins as the ones found in the previous paragraph.
Second, it is necessary to add the following instruction right **after** the `kubernetes:kubernetes` line:
```
...
kubernetes:kubernetes
multicluster:github.com/coredns/multicluster
...
```
Then trigger the recompilation:

```
$ docker run --rm -i -t -v $PWD:/v -w /v golang:1.18 make
```

Once you have recompiled CoreDNS with the multicluster plugin, you can then build the new container image.

```
sudo docker buildx build --platform linux/amd64 . -t [your-image-registry-path]:with-mcs-plugin
```

Then push the image to your registry.

```
docker push [your-image-registry-path]:with-mcs-plugin
```

## Deploying the multicluster-enabled CoreDNS image
The new CoreDNS with multicluster plugin enabled is now ready to be deployed. However, this new component will require some extra RBAC roles in order to query the Kubernetes API to discover ServiceImport objects, and a modification of its configuration file (Corefile) stored in the `coredns` ConfigMap object.

### Deploy the Multicluster-related CRDs

```
kubectl apply -f https://github.com/kubernetes-sigs/mcs-api/blob/master/config/crd/multicluster.x-k8s.io_serviceexports.yaml
kubectl apply -f https://github.com/kubernetes-sigs/mcs-api/blob/master/config/crd/multicluster.x-k8s.io_serviceimports.yaml
```

### Setting up RBAC roles for CoreDNS
Create a new ClusterRole and bind it to the `coredns` Service Account.

```
cat <<EOF > coredns-multicluster-rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:coredns-multicluster
rules:
- apiGroups:
  - "multicluster.x-k8s.io"
  resources:
  - serviceimports
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: system:coredns-multicluster
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:coredns-multicluster
subjects:
- kind: ServiceAccount
  name: coredns
  namespace: kube-system
EOF
```
then apply the manifest.

```
kubectl apply -f ./coredns-multicluster-rbac.yaml
```

### Update the ConfigMap with the CoreDNS Corefile
The CoreDNS Corefile includes the configuration of CoreDNS running on the cluster.

You need to edit the ConfigMap to add the `multicluster clusterset.local` line before the `kubernetes cluster.local...` line.

```
        ...
        multicluster clusterset.local
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        ...
```

then perform a `rollout restart` of the `coredns` deployment so that CoreDNS can take this new configuration into account.

```
kubectl rollout restart deploy coredns -n kube-system
```

### Re-deploy CoreDNS
Save the current configuration of the CoreDNS deployment, and delete it from the cluster.

```
kubectl get deploy coredns -n kube-system -o yaml > coredns-deploy.yaml
kubectl delete deploy coredns
```

Replace the image path in the deployment manifest with the one you previously pushed to your image registry, and re-deploy the manifest. The new pods will restart with the new configuration stored in the Config Map previously modified.

### Verify that CoreDNS is healthy

```
kubectl get pods -n kube-system
```

**Output (Do Not Copy)**
```
kubectl get pods -n kube-system
NAME                                              READY   STATUS    RESTARTS   AGE
coredns-55fcfcb54f-lg25c                          1/1     Running   0          25s
coredns-55fcfcb54f-ts9sp                          1/1     Running   0          25s
etcd-cluster-1-control-plane                      1/1     Running   0          38m
kindnet-wd847                                     1/1     Running   0          38m
kube-apiserver-cluster-1-control-plane            1/1     Running   0          39m
kube-controller-manager-cluster-1-control-plane   1/1     Running   0          38m
kube-proxy-n9ds4                                  1/1     Running   0          38m
kube-scheduler-cluster-1-control-plane            1/1     Running   0          39m
```

## More steps when you want to check that the multicluster plugin works

Create a demo namespace and deploy a fake ServiceImport.

```
cat <<EOF > demo-service-import.yaml
apiVersion: multicluster.x-k8s.io/v1alpha1
kind: ServiceImport
metadata:
  name: myservice
  namespace: demo
spec:
  type: ClusterSetIP
  ips:
  - 1.2.3.4
  ports:
  - port: 80
    protocol: TCP
EOF
```
```
kubectl apply -f demo-service-import.yaml
```

Then deploy a `dnsutils` pod in the demo namespace.

```
cat <<EOF > dnsutils.yaml
apiVersion: v1
kind: Pod
metadata:
  name: dnsutils
  namespace: demo
spec:
  containers:
  - name: dnsutils
    image: k8s.gcr.io/e2e-test-images/jessie-dnsutils:1.3
    command:
      - sleep
      - "3600"
    imagePullPolicy: IfNotPresent
  restartPolicy: Always
EOF
```

```
kubectl apply -f dnsutils.yaml
```

You can then use the `dnsutils` pod to confirm that the DNS query for the ServiceImport responds with the IP set in the fake ServiceImport previously defined.

```
kubectl exec -it dnsutils -n demo -- bash
```
```
root@dnsutils:/# nslookup myservice.demo.svc.clusterset.local
```
**Output (Do Not Copy)**
```
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	myservice.demo.svc.clusterset.local
Address: 1.2.3.4
```