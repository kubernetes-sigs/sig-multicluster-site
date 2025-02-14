# Implementations

This document tracks downstream implementations and integrations of Multicluster API and provides status and resource references for them.

Implementors and integrators of Multicluster API are encouraged to update this document with status information about their implementations, the versions they cover, and documentation to help users get started.

## Implementation Status

- [Google Cloud MCS][gke-mcs]: General Availability
- [Submariner][submariner]: 0.13.3
- [MCS controller for AWS Cloudmap][aws-mcs]: Alpha
- [Antrea Multi-cluster][antrea-mcs]: Alpha
- [Cilium Cluster Mesh][cilium-clustermesh]: Beta (from Cilium v1.17)

## Implementations

In this section you will find specific links to blog posts, documentation and other Multicluster API references for specific implementations.


### Google Kubernetes Engine

[Google Kubernetes Engine (GKE)][gke] is a managed Kubernetes platform offered by Google Cloud. GKE's implementation of the Multicluster API is through the [GKE Multi Cluster Service][gke-mcs].

[gke]:https://cloud.google.com/kubernetes-engine
[gke-mcs]:https://cloud.google.com/kubernetes-engine/docs/concepts/multi-cluster-services

Please follow this [guide][gke-mcs-guide] for the first steps to set up multicluster services on GKE.

[gke-mcs-guide]:gke-mcs.md

### Submariner

[Submariner][submariner] is an open-source project enabling direct networking between Pods and Services in different Kubernetes clusters, either on-premises or in the cloud.
Submariner provides:

- Cross-cluster L3 connectivity using encrypted and unencrypted connections
- Service Discovery across clusters
- `subctl`, a command-line utility that simplifies deployment and management
- Support for interconnecting clusters using overlapping CIDRs

[submariner]: https://submariner.io/

### MCS controller for AWS Cloudmap
The [AWS Cloud Map Multi-cluster Service Discovery Controller for Kubernetes (K8s)][aws-mcs] implements the Kubernetes [KEP-1645: Multi-Cluster Services API][kep-1645] and [KEP-2149: ClusterId for ClusterSet identification][kep-2149], which allows services to communicate across multiple clusters. The implementation relies on AWS Cloud Map for enabling cross-cluster service discovery.

Please follow this [guide][aws-mcs-guide] for the first steps to set up the multicluster controller.

[aws-mcs]: https://github.com/aws/aws-cloud-map-mcs-controller-for-k8s
[aws-mcs-guide]: https://aws.github.io/aws-cloud-map-mcs-controller-for-k8s/
[kep-1645]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-multicluster/1645-multi-cluster-services-api
[kep-2149]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-multicluster/2149-clusterid

### Antrea Multi-cluster

[Antrea][antrea] is an open-source project which is a Kubernetes networking solution intended to be Kubernetes native. It operates at Layer 3/4 to provide networking and security services for a Kubernetes cluster, leveraging Open vSwitch as the networking data plane.

[Antrea Multi-cluster][antrea-mcs-arch] implements Multi-cluster Service API, which allows users to create multi-cluster Services that can be accessed cross clusters in a ClusterSet. Antrea Multi-cluster also extends Antrea native NetworkPolicy to support [Multi-cluster NetworkPolicy][antrea-mcs-anp] rules that apply to cross-cluster traffic, and [ClusterNetworkPolicy replication][antrea-mcs-cnp-replica] that allows a ClusterSet admin to create ClusterNetworkPolicies which are replicated across the entire ClusterSet and enforced in all member clusters.

Please follow this [guide][antrea-mcs-user-guide] for the first steps to set up Antrea Multi-cluster.

[antrea]: https://antrea.io/
[antrea-mcs]: https://github.com/antrea-io/antrea/tree/main/multicluster
[antrea-mcs-arch]: https://github.com/antrea-io/antrea/blob/main/docs/multicluster/architecture.md
[antrea-mcs-cnp-replica]: https://github.com/antrea-io/antrea/blob/main/docs/multicluster/user-guide.md#clusternetworkpolicy-replication
[antrea-mcs-anp]: https://github.com/antrea-io/antrea/blob/main/docs/multicluster/user-guide.md#multi-cluster-networkpolicy
[antrea-mcs-user-guide]: https://github.com/antrea-io/antrea/blob/main/docs/multicluster/user-guide.md

### Cilium Cluster Mesh

[Cilium][cilium] is an open source, cloud native solution for providing, securing, and observing network connectivity between workloads, fueled by the Kernel technology eBPF.

[Cilium Cluster Mesh][cilium-clustermesh] allows you to connect the networks of multiple clusters in such as way that pods in each cluster can discover and access services in all other clusters of the mesh, provided all the clusters run Cilium as their CNI. This allows effectively joining multiple clusters into a large unified network, regardless of the Kubernetes distribution or location each of them is running.

Starting with Cilium version 1.17, Cilium Cluster Mesh also supports MCS-API; see the corresponding [guide][cilium-mcs] for more information!

[cilium]: https://cilium.io/
[cilium-clustermesh]: https://cilium.io/use-cases/cluster-mesh/
[cilium-mcs]: https://docs.cilium.io/en/stable/network/clustermesh/mcsapi/
