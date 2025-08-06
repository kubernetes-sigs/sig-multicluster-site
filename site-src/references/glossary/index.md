# Glossary

About API: A cluster-local CRD to store arbitrary properties about a cluster.
See [About API Overview](concepts/about-api.md).

ClusterProfile API: A CRD intended to store information about member clusters in
a clusterset. See [ClusterProfile API Overview](concepts/clusterprofile-api.md).

ClusterSet: A group of clusters governed by a single authority, with a high
degree of trust, and in which namespace sameness applies. See [ClusterSet
reference](api-types/clusterset.md).

Multicluster Services API: An CRD composed of the ServiceExport and
ServiceImport Kinds, used to facilitate accessing Services across clusters. See
[Multicluster Services API Overview](concepts/multicluster-services-api.md).

Namespace Sameness: A property of clusters in clustersets, in which Kubernetes
objects of the same name in the same namespace are expected to behave similarly
across the clusterset. See [Namespace Sameness
reference](api-types/namespace-sameness.md).

Work API: A CRD defining the Work Kind, intended to facilitate distributing
workloads across multiple clusters. See [Work API
Overview](concepts/work-api.md).
