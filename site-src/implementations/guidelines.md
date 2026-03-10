# Implementation guidelines

There are some general guidelines for implementers of SIG-Multicluster sponsored
APIs.


## Conformance Expectations

We expect there will be varying levels of conformance among the different
providers for some time. SIG-Multicluster is currently working on the framework
for a conformance suite so implementations can test their conformance to the API
specifications in an automated way. For now, each individual KEP indicates what
a conformant implementation of a given API  "MUST", "MAY", and "SHOULD" adhere
to, following the interpretations of those terms as described in RFC 2119.


### Implementation-specific

In some aspects of the APIs, the specification provides the general user usage
pattern of a feature, however, the exact behavior may depend on the underlying
implementation. When known, these are called out in the KEP as implementation
details to clearly distinguish between conformance expectations and the
variations in behavior that are considered "implementation-specific".


## API Conventions

SIG-Multicluter sponsored APIs follow Kubernetes API [conventions]. These
conventions are intended to ease client development and ensure that
configuration mechanisms can consistently be implemented across a diverse set of
use cases. 

[conventions]:(https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)


## API Process

SIG-Multicluster sponsored APIs are communicated and matured via the [Kubernetes
Enhancements Proposal process][KEPs], regardless of whether they are implemented as
part of a Kubernetes release. SIG-sponsored artifacts such as conformance tests,
published CRD yaml, or related images or software are published in repos in the
[Kubernetes-sigs Github organization][kubernetes-sigs].

[KEPs]: (https://github.com/kubernetes/enhancements/tree/master/keps/sig-multicluster)
[kubernetes-sigs]: (https://github.com/kubernetes-sigs/)

## Limitations of CRD and Webhook Validation

CRD and webhook validation is not the final validation i.e. webhook is "nice UX"
but not schema enforcement. This validation is intended to provide immediate
feedback to users when they provide an invalid configuration. Write code
defensively with the assumption that at least some invalid input will reach your
controller. Both Webhook and CRD validation is not fully reliable because it:

* May not be deployed correctly.
* May be loosened in future API releases. (Fields may contain values with less
  restrictive validation in newer versions of the API). 

*Note: These limitations are not unique to SIG-Multicluster sponsored APIs and
apply more broadly to any Kubernetes CRDs and webhooks.*

Implementers should ensure that, even if unexpected values are encountered in
the API, their implementations are still as secure as possible and handle this
input gracefully. The most common response would be to reject the configuration
as malformed and signal the user via a condition in the status block. To avoid
duplicating work, Multicluster API maintainers are considering adding a shared
validation package that implementations can use for this purpose.
