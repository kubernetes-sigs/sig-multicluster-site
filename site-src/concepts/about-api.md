# About API Overview

This document provides an overview of the About API.

![Alt](../images/about-api.png "About API")

The About API allows metadata to be attached to individual clusters.
The fundamental resource defined in the API is the ClusterProperty CRD.

You can read more details about the API in [KEP-2149](https://github.com/kubernetes/enhancements/tree/master/keps/sig-multicluster/2149-clusterid).

## ClusterProperty CRD

The ClusterProperty CRD is proposed to give a Kubernetes-native way of identifying clusters, however, it can be used to store any metadata about a cluster.

### Example

```yaml
apiVersion: about.k8s.io/v1beta1
kind: ClusterProperty
metadata:
  # The name serves as the property key
  # This example uses a well-known reserved key for cluster identification
  # Format: cluster.clusterset.k8s.io (reserved for cluster identification)
  # Note: Keys under *.k8s.io and *.kubernetes.io are reserved
  # User-defined properties should use other suffixes
  name: cluster.clusterset.k8s.io
spec:
  # The property value (must be a string)
  # In this case, "cluster-1" is the unique identifier for this cluster
  # This could be any string value that identifies or describes the cluster
  value: cluster-1
```

In the above example the ClusterProperty CRD is used to identify a cluster with the id of `cluster-1`. The key in this example `cluster.clusterset.k8s.io`, is one of the two proposed well-known properties.

### Well-known properties

There are two well-known properties proposed:

#### 1. `cluster.clusterset.k8s.io` — Cluster ID

##### Uniqueness

* **Required:** Unique **within its ClusterSet**.
* **Optional:** May also be globally unique across ClusterSets.
* **Optional:** May remain unique across the lifetime of the physical/virtual cluster (beyond membership changes).

##### Lifespan

* **Required:** Exists and is **immutable** while the cluster is a member of a ClusterSet.
* **Condition:** Maintained as long as a corresponding `clusterset.k8s.io` property exists.

##### Contents

* **Required:** A DNS subdomain per **RFC 1123**.
* **Recommended:** Fewer than 128 characters.
* **Usable as:** A component of **MCS DNS** names.
* **Optional:** A human-readable cluster name (as long as it is a valid RFC 1123 subdomain).

##### Consumers

* **May rely** on immutability of the ID during ClusterSet membership.
* **Should watch** for changes after the cluster leaves a ClusterSet (e.g., to detect reassignment).
* **May use** on non-member clusters if an implementation populates it.

##### Notable scenarios

* **Re-use on rejoin:** After leaving a ClusterSet, a cluster may rejoin using the same ID.
* **Re-assignment:** A different cluster may be assigned the same ID **after** the original cluster has left the ClusterSet (never concurrently within the same ClusterSet).

##### Constraints / Non-goals

* No guarantee of **global** uniqueness.
* Immutable while a **member**; may be reassigned **after** leaving a ClusterSet.
* No standardized **aliasing**/alternate-name mechanism.

#### 2. `clusterset.k8s.io` — ClusterSet membership

##### Lifespan

* **Required:** Exists and is **immutable** while the cluster belongs to a ClusterSet.
* **Required:** **Must not exist** when the cluster is not a member of any ClusterSet.

##### Contents

* **Required:** An identifier that associates the cluster with a specific ClusterSet.

##### Consumers

* May rely on immutability during membership.
* Should watch the property to detect **join**, **move**, or **leave** events.

##### Constraints / Non-goals

* A cluster belongs to **exactly one** ClusterSet at a time; **concurrent multi-membership is not supported**.
* Admission control may detect duplicate/conflicting settings, but **automatic conflict resolution** is out of scope.

### Common use cases

* **Multi-Cluster Services (MCS) DNS partitioning**
  Distinguish endpoints of headless Services per cluster using the Cluster ID.
  Example: `clusterA.myservice.test.svc.clusterset.local.`

* **Observability tagging (logging/metrics/tracing)**
  Attach `clusterId` / `ClusterSet` to telemetry to make the source cluster explicit.

* **Multi-cluster-aware controllers**
  Use properties to drive per-cluster logic or to select target clusters.

* **Lifecycle visibility for ClusterSet management**
  Detect ClusterSet **join/move/leave** from presence/changes in `clusterset.k8s.io`.

### Notes on identifiers

* UUID-style IDs reduce collision risk but are less ergonomic as DNS names.
* Human-readable names are friendly but risk collisions; using DNS-compliant names can help align with MCS DNS.
* Combining DNS-friendly and UUID identifiers is left to implementations.

### Operational guidance

* **Immutability:** Do not change `cluster.clusterset.k8s.io` while a cluster is a member of a ClusterSet.
* **Uniqueness enforcement:** Use admission control to prevent duplicate IDs **within a ClusterSet**.
* **Choosing IDs:** Balance readability vs. collision avoidance depending on your environment.
* **Separation of duties:** Each property is its own resource; use **RBAC** to control who can create/update specific properties.
