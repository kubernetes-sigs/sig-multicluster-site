# Glossary

About API: An API that defines the cluster-scoped ClusterProperty resource for
storing properties about a cluster. See [About API
Overview](../../concepts/about-api.md).

Cluster Inventory: The ClusterProfile objects in one namespace. See
[ClusterProfile API
Overview](../../concepts/cluster-profile-api.md#cluster-inventories).

ClusterProfile API: An API that defines namespace-scoped ClusterProfile
resources for describing member clusters in an inventory. See [ClusterProfile
API Overview](../../concepts/cluster-profile-api.md).

ClusterSet: A group of clusters governed by a single authority, with a high
degree of trust, and in which namespace sameness applies. See [ClusterSet
reference](../../api-types/cluster-set.md).

Multicluster Services API: An API composed of the ServiceExport and
ServiceImport kinds, used to access Services across clusters. See [Multicluster
Services API Overview](../../concepts/multicluster-services-api.md).

Namespace Sameness: A property of clusters in ClusterSets, in which Kubernetes
objects of the same name in the same namespace are expected to behave similarly
across the ClusterSet. See [Namespace Sameness
reference](../../concepts/namespace-sameness.md).

Work API: A CRD defining the Work Kind, intended to facilitate distributing
workloads across multiple clusters. See [Work API
Overview](../../concepts/work-api.md).
