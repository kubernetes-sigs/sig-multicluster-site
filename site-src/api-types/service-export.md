# ServiceExport

## Resource Definition
A ServiceExport is a Customer Resource Definition used to specify which Kubernetes Services should be exported within a cluster.

A ServiceExport resource is created with the cluster and namespace that a given Service resides in, and is name-mapped to the service for export. In other words, the ServiceExport is referenced with the same name as the export.

If multiple clusters export a Service with the same namespaced name, they will be recognized as a single combined service.

## DNS
When a ServiceExport is created, this will cause a domain name for the multi-cluster service to become accessible from within the ClusterSet. The domain name will be `<service-export-name>.<service-export-namespace>.svc.clusterset.local`.

## EndPointSlice
When a ServiceExport is created, this will cause EndpointSlice objects for the underlying Service to be created in each cluster within the ClusterSet. One or more EndpointSlice resources will exist for each cluster that exported the Service, with each EndpointSlice containing only endpoints from its source cluster. These EndpointSlice objects are  marked as managed by the ClusterSet service controller, so that the endpoint slice controller doesn’t delete them.