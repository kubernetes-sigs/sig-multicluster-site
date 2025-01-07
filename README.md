# SIG-Multicluster website

This repo holds and hosts the site for [SIG-Multicluster](https://multicluster.sigs.k8s.io/),
a special interest group of the Kubernetes project.

## Community, discussion, contribution, and support

Learn how to engage with the Multicluster Special Interest Group community on the
[community page](https://github.com/kubernetes/community/tree/master/sig-multicluster#multicluster-special-interest-group/).

You can reach the maintainers of this project at:

- Slack: [#sig-multicluster](https://kubernetes.slack.com/messages/sig-multicluster/)
- [Mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-multicluster/)

### Code of conduct

Participation in the Kubernetes community is governed by the [Kubernetes Code of Conduct](code-of-conduct.md).

[owners]: https://git.k8s.io/community/contributors/guide/owners.md
[Creative Commons 4.0]: https://git.k8s.io/website/LICENSE

# Contributors

## Install and run

Install Python and the requirements for this site using the included `Makefile`.

  ```
    make install
  ```

Use the mkdocs CLI to serve a development version of the site.

  ```mkdocs serve```

Navigate to `localhost:8000` to see the site.

## Build and deploy

Use the mkdocs CLI to deploy to the `gh-pages` branch of the repo.

   ```mkdocs gh-deploy```
