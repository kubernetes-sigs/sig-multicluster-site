# Introduction

Since its inception in 2015, Kubernetes has been pretty successful at popularizing the idea of container clusters.  Adoption has reached the point that many users are deploying their applications across multiple clusters and are struggling to make it work smoothly. 

SIG-Multicluster is a [Special Interest Group][sig-multicluster-github] focused on solving common challenges related to the management of multiple Kubernetes clusters, and applications that exist therein. 

Specifically, the SIG aims to fine Kubernetes-native ways to:

* Expose workloads from multiple clusters to each other
* Share cluster metadata and its place relative to others
* Generally break down the walls between clusters

The SIG is responsible for designing, discussing, implementing and maintaining API’s, tools and documentation related to multi-cluster administration and application management. This includes not only active automated approaches such as Cluster Federation, but also those that employ batch workflow-style continuous deployment systems like Spinnaker and others. Standalone building blocks for these and other similar systems (for example a cluster registry), and proposed changes to kubernetes core where appropriate will also be in scope.

## Problem statement: why multicluster?

There are many reasons to want to run multiple clusters, including but not limited to:

* Location
    * Latency: it can be necessary to deploy the application as close to the customers as possible.
    * Jurisdiction: it can be mandated to keep user data in-country.
    * Data gravity: data already exists in one provider, but it can be decided to run the application in another environment.

* Isolation
    * Environment (e.g. dev, test, prod)
    * Performance isolation: a workload may consume too many resources, at the expense of other workloads. 
    * Security isolation: sensitive data or untrusted code must be isolated in their own environments.
    * Organizational isolation: teams may have different management domains.
    * Cost isolation: multitenancy can greatly complexify billing management for different teams.

* Reliability
    * Blast radius: an infrastructure or application incident in one cluster must not impact the whole system.
    * Infrastructure diversity: an underlying zone, region, or provider outage does not bring down the whole system.
    * Scale: the application is too big to fit in a single cluster.
    * Upgrade scope: some parts of the application may require an infrastructure upgrade, that may impact other parts of the application. Having multiple clusters can also avoid the need for in-place cluster upgrades.

## Project charter
The following charter defines the scope and governance of the [Multicluster Special Interest Group][sig-multicluster-github]:

* Support an out-of-tree ecosystem by defining API standards that leave plenty of rool for flexibility in their ultimately third party implementation.

* Protect the known multicluster experience from incompatible changes upstream to single clusters by working with other [SIGs][sigs-github].

* Advocate and provide feedback on proposals for extending the single cluster experience to multicluster i.e. network policy.

[sig-multicluster-github]:  https://github.com/kubernetes/community/tree/master/sig-multicluster
[sigs-github]: https://github.com/kubernetes-sigs



## Approach

To meet the goals listed above, the SIG-Multicluster team has worked to define three different APIs:

* [About API][about-api-reference]: allows to uniquely identify clusters within a set of clusters ([clusterset][clusterset-definition])
* [Multicluster Services API][mc-api-reference]: allows to expose services across clusters which are part of a given [clusterset][clusterset-definition].
* [Work API][work-api-reference]: allows to define the workloads to be deployed across clusters which are part of a given [clusterset][clusterset-definition].

[about-api-reference]: ./concepts/about-api.md
[mc-api-reference]: ./concepts/multicluster-services-api.md
[work-api-reference]: ./concepts/work-api.md
[clusterset-definition]: ./api-types/cluster-set.md

To leave room for implementation, SIG-Multicluster does not focus on the implementation of the mechanisms that rely on those APIs. For example, no reference implementation is provided for a cluster registry or for service discovery itself.

# Getting started
Whether you are a user interested in using the different APIs or an implementer interested in conforming to the APIs, the following resources will help give you the necessary background:

* [KubeCon NA 2022 "SIG-Multicluster Intro and Deep Dive"][kubecon-na-2022-video] by Laura Lorenz (Google), Jeremy Olmsted-Thompson (Google) and Paul Morie (Apple) 

[![Watch the video](https://img.youtube.com/vi/VZnF3YO1cm8/hqdefault.jpg)](https://www.youtube.com/watch?v=VZnF3YO1cm8)

* [Implementation guide and references][implementation-index]

[kubecon-na-2022-video]: https://www.youtube.com/watch?v=VZnF3YO1cm8
[implementation-index]: ./guides/index.md

* [Community links][get-involved]

# Contributing
If you are interested in contributing to SIG-Multicluster or building an implementation of one of our APIs, then don’t hesitate to [get involved][get-involved] in SIG meetings, issues on projects, or new designs.

[get-involved]: ./contributing/index.md