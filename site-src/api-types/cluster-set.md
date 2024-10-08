# ClusterSet

ClusterSet represents a specific pattern implemented by various organizations. A ClusterSet is typically:

- A group of clusters governed by a single authority.
- There is usually a high degree of trust within the set of clusters.
- [Namespace Sameness](../concepts/namespace-sameness.md) applies to clusters in the set:
    - Permissions and characteristics are consistent across clusters for a given namespace.
    - Namespaces don't have to exist in every cluster, but behave the same across those in which they do.

!!!note
    The early definition of the ClusterSet was described in [KEP-2149](https://github.com/kubernetes/enhancements/tree/master/keps/sig-multicluster/2149-clusterid). It is now part of the [About API](https://sigs.k8s.io/about-api).

A cluster's ClusterSet membership is stored in the about.k8s.io/ClusterProperty `clusterset.k8s.io`.

## Cluster Metadata
The ClusterSet is a Cluster-scoped ClusterProperty CRD (Customer Resource Definition), that stores a name and a value.

This property can be used to:

- uniquely identify clusters using a clusterID

    ```
    apiVersion: about.k8s.io/v1alpha1
    kind: ClusterProperty
    metadata:
        name: cluster.clusterset.k8s.io
    spec:
        value: cluster-1
    ```

- uniquely identify the membership of a cluster in a ClusterSet for the lifetime of the membership.

    ```
    apiVersion: about.k8s.io/v1alpha1
    kind: ClusterProperty
    metadata:
        name: clusterset.k8s.io
    spec:
        value: mycoolclusterset
    ```

- Provide a reference point for multi-cluster tooling to build on within a cluster set, for example for DNS labels, for logging and tracing, etc.

- Provide extra metadata space to store other cluster properties that might otherwise be implemented as ad-hoc annotations on semantically adjacent objects.

    ```
    apiVersion: about.k8s.io/v1alpha1
    kind: ClusterProperty
    metadata:
        name: fingerprint.mycoolimplementation.com
    spec:
        value:  '{"major": "1","minor": "18","gitVersion": "v1.18.2","gitCommit": "52c56ce7a8272c798dbc29846288d7cd9fbae032","gitTreeState": "clean","buildDate": "2020-04-30T20:19:45Z","goVersion": "go1.13.9","compiler": "gc","platform": "linux/amd64"}'
    ```
