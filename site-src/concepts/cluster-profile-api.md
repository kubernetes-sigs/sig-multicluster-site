# ClusterProfile API Overview

This document provides an overview of the [ClusterProfile API](https://github.com/kubernetes-sigs/cluster-inventory-api?tab=readme-ov-file#cluster-profile-api).

![Alt](../images/cluster-profile-api.png "ClusterProfile API")

A Cluster Profile is a namespace-level resource and essentially represents an individual member of the Cluster Inventory
that details properties and status of a cluster. This API proposes a standardized interface that defines how cluster information should be presented
and interacted with across different platforms and implementations.

You can read more details about the API in the [KEP-4322](https://github.com/kubernetes/enhancements/blob/master/keps/sig-multicluster/4322-cluster-inventory/README.md).

## Terminology

- **Cluster Inventory**: A conceptual term referring to a collection of clusters. A cluster inventory may or may not represent
a [ClusterSet](../api-types/cluster-set.md). A cluster inventory is considered a clusterSet if all its member clusters adhere to the 
[namespace sameness](https://github.com/kubernetes/community/blob/master/sig-multicluster/namespace-sameness-position-statement.md) principle.

- **Cluster Manager**: An entity that creates the ClusterProfile API object per member cluster,
  and keeps their status up-to-date. Each cluster manager MUST be identified with a unique name.  
  Each ClusterProfile resource SHOULD be managed by only one cluster manager. A cluster manager SHOULD
  have sufficient permission to access the member cluster to fetch the information so it can update the status
  of the ClusterProfile API resource.

- **ClusterProfile API Consumer**: the person running the cluster managers
  or the person developing extensions for cluster managers for the purpose of
  workload distribution, operation management etc.

## Access to member clusters (`status.accessProviders`)

ClusterProfile describes a cluster, but it does not itself define a single universal way to authenticate to that cluster.
Different environments use different credential sources (cloud IAM tokens, in-cluster Secrets, external identity systems, etc.).

To make multicluster controllers interoperable, `status.accessProviders` standardizes the **reachability details** for a cluster
and provides enough information for a consumer to select an **external credentials provider** mechanism (plugin) to obtain credentials.

- **What `accessProviders` is**: A list of named access provider entries. Each entry represents one way a consumer can connect to the member cluster.
  - **`name`**: The access provider type identifier (for example `google` or `secretreader`). Consumers can use this value to select a matching credential provider plugin.
  - **`cluster`**: Connection details that reuse the kubeconfig `Cluster` schema (for example `server`, `certificate-authority-data`, `proxy-url`).

- **What `accessProviders` is not**: It is **not** a place to store credentials. Tokens, client certs, and other secrets should not appear in ClusterProfile.
  Consumers are expected to obtain credentials out-of-band, typically via an exec-style credential provider plugin as described in
  [KEP-5339](https://github.com/kubernetes/enhancements/blob/master/keps/sig-multicluster/5339-clusterprofile-plugin-credentials/README.md).

### Selecting an access provider

`status.accessProviders` is written by the cluster manager (or its extensions) and treated as read-only by consumers.
If multiple access providers are present, consumers typically select an entry by `name` based on what credential provider plugins they support.

### Plugin configuration (`cluster.extensions`)

Some credential providers need extra parameters (for example a `clusterName`) in order to fetch credentials.
These parameters should be **per-cluster** and **non-secret**, and must not include controller- or environment-specific data.
When plugin-specific per-cluster configuration is needed, use the Kubernetes client authentication API exec plugin mechanism.
See the reference for the exact schema and semantics:
[client authentication API: `Cluster.config` for exec plugins](https://kubernetes.io/docs/reference/config-api/client-authentication.v1/#client-authentication-k8s-io-v1beta1-Cluster)

## API Example

[CRD definition](https://github.com/kubernetes-sigs/cluster-inventory-api/blob/main/config/crd/bases/multicluster.x-k8s.io_clusterprofiles.yaml)

```yaml
apiVersion: multicluster.x-k8s.io/v1alpha1
kind: ClusterProfile
metadata:
  name: some-cluster-name
  namespace: fleet-system
  labels:
    x-k8s.io/cluster-manager: some-cluster-manager
spec:
  displayName: some-cluster
  clusterManager:
    name: some-cluster-manager
status:
  version:
    kubernetes: 1.28.0
  properties:
    - name: clusterset.k8s.io
      value: some-clusterset
    - name: location
      value: apac
  accessProviders:
    - name: secretreader
      cluster:
        server: https://api.some-cluster.example:6443
        certificate-authority-data: <base64-encoded-ca>
        extensions:
          - name: client.authentication.k8s.io/exec
            extension:
              clusterName: some-cluster-name
  conditions:
    - type: ControlPlaneHealthy
      status: True
      lastTransitionTime: "2023-05-08T07:56:55Z"
      message: ""
    - type: Joined
      status: True
      lastTransitionTime: "2023-05-08T07:58:55Z"
      message: ""
```
