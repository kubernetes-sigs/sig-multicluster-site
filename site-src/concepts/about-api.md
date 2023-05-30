# About API Overview

A cluster-scoped CRD to store arbitrary data about a cluster in one place.

* Full definition in [KEP-2149](https://github.com/kubernetes/enhancements/tree/master/keps/sig-multicluster/2149-clusterid)
* CRD available at [sigs.k8s.io/about-api](https://github.com/kubernetes-sigs/about-api)

## Overview

When you need to store arbitrary data about a cluster in the Kubernetes API, you can install the About API. This API contains one flexible Kind, the `ClusterProperty`, defined by a simple schema comprised of just `metadata.name` and a `spec.value`, which you can use to store or expose any cluster-scoped metadata. 

Some resource names, described below in [Well known properties](#well-known-properties), are reserved and must behave in certain ways when present as they are used as a reference for multi-cluster tooling to build on within a cluster set.

Any other resources names are allowed so long as they do not conflict with the well known properties _and_ utilize a suffix. The following suffixes are reserved for Kubernetes and related projects: `.k8s.io`, `.kubernetes.io`.

```yaml
# examples
apiVersion: about.k8s.io/v1
kind: ClusterProperty
metadata:
  name: fingerprint.mycoolimplementation.com
spec:
  value:  '{"major": "1","minor": "18","gitVersion": "v1.18.2","gitCommit": "52c56ce7a8272c798dbc29846288d7cd9fbae032","gitTreeState": "clean","buildDate": "2020-04-30T20:19:45Z","goVersion": "go1.13.9","compiler": "gc","platform": "linux/amd64"}'
---
apiVersion: about.k8s.io/v1
kind: ClusterProperty
metadata:
  name: environment.trainingapp.fundatacompany.com
spec:
  value:  'staging'
---
apiVersion: about.k8s.io/v1
kind: ClusterProperty
metadata:
  name: distribution.anothercloudvendor.com
spec:
  value:  'Kubernetes Plus Plus Plus With Stars And Hearts'
```


## FAQ

### When should I use the About API instead of annotations?

Annotations must be applied to a Kubernetes resource. If there is not already a Kubernetes resource you prefer to attach your annotation to, you should use the About API instead. 

Also consider using the About API if the Kubernetes resource you already use or plan to use is outside your control or only a "good enough" semantic fit for your use case. A common example is adding annotations on `Node` objects from the core API to store metadata about the cluster, but this is inconvenient or impossible when seeking to store metadata that might exist before any nodes or `Node` objects are provisioned.

In addition, the About API being implemented as a CRD gives it access to richer tooling than the annotations API was designed for. Implementations dependent on annotations eventually develop annotation libraries wrapping the basic GetAnnotations() method of generated clients to query and enforce business logic.  Annotations cannot be watched individually. Annotations cannot have RBAC applied independently of the parent resource. 

### When should I use the About API instead of making my own CRD?

If you already have or need to make your own CRD for the implementation of your feature, it is likely more appropriate for the metadata to be represented there. If you want some metadata to be published to tooling that already depends on the About API, you might consider storing it there instead or mirroring the part of it that is relevant to publish from your more metadata-rich implementation-specific CRD.


## Well known properties

#### Property: `cluster.clusterset.k8s.io`

Contains a unique identifier for the containing cluster.

##### Uniqueness

*   The identifier **must** be unique within the ClusterSet to which its cluster belongs for the duration of the cluster’s membership.
*   The identifier **should** be unique beyond the ClusterSet within the scope of expected use.
*   The identifier **may** be globally unique beyond the scope of its ClusterSet.
*   The identifier **may** be unique beyond the span of its cluster’s membership and lifetime.


##### Lifespan

*   The identifier **must** exist and be immutable for the duration of a cluster’s membership in a ClusterSet, and as long as a `clusterset.k8s.io` property referring to that cluster in that ClusterSet exists.
*   The identifier **must** exist for the lifespan of a cluster.
*   The identifier **should** be immutable for the lifespan of a cluster.


##### Contents

*   The identifier **must** either:
    *   be a valid [RFC-1123](https://tools.ietf.org/html/rfc1123) DNS label,
    *   or be composed of two valid [RFC-1123](https://tools.ietf.org/html/rfc1123) DNS labels separated with a dot.
*   The identifier **may** be used as a component in MCS DNS.
*   The identifier **may** be a human readable description of its cluster.


##### Consumers

*   **Must** be able to rely on the identifier existing, unmodified for the entire duration of its membership in a ClusterSet.
*   **Should** watch the `cluster.clusterset.k8s.io` property to handle potential changes if they live beyond the ClusterSet membership.
*   **May** rely on the existence of an identifier for clusters that do not belong to a ClusterSet so long as the implementation provides one.

```yaml
# example cluster.clusterset.k8s.io ClusterProperty
apiVersion: about.k8s.io/v1
kind: ClusterProperty
metadata:
  name: cluster.clusterset.k8s.io
spec:
  value: cluster-1
```

#### Property: `clusterset.k8s.io`

Contains an identifier that relates the containing cluster to the ClusterSet in which it belongs.


##### Lifespan

*   The identifier **must** exist and be immutable for the duration of a cluster’s membership in a ClusterSet.
*   The identifier **must not** exist when the cluster is not a member of a ClusterSet.


##### Contents

*   The identifier **must** associate the cluster with a ClusterSet.
*   The identifier **may** be either unique or shared by members of a ClusterSet.


##### Consumers

*   **Must** be able to rely on the identifier existing, unmodified for the entire duration of its membership in a ClusterSet.
*   **Should** watch the clusterset property to detect the span of a cluster’s membership in a ClusterSet.

```yaml
# example clusterset.k8s.io ClusterProperty
apiVersion: about.k8s.io/v1
kind: ClusterProperty
metadata:
  name: clusterset.k8s.io
spec:
  value: mycoolclusterset
```
