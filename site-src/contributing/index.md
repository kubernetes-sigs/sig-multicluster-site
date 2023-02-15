# How to Get Involved

This page contains links to all of the meeting notes, design docs and related discussions around the different APIs managed by the Multicluster SIG.

## Feedback and Questions

For general feedback, questions or to share ideas please feel free to [create a
new discussion against the site repo][gh-disc].
[gh-disc]:https://github.com/lauralorenz/sig-multicluster-site-proposal/discussions/new

## Bug Reports

Bug reports should be filed as Github Issues on their respective subproject repo.

* [Open an issue for a bug with the About API][about-api-issues]
* [Open an issue for a bug with the MCS API][mcs-api-issues]
* [Open an issue for a bug with the Work API][work-api-issues]

**NOTE**: If you're reporting a bug that applies to a specific implementation of
a SIG-MC sponsored API and not the API specification itself, please check our
[implementations page][implementations] to find links to the repositories where
you can get help with your specific implementation.
[about-api-issues]: https://github.com/kubernetes-sigs/about-api/issues
[mcs-api-issues]: https://github.com/kubernetes-sigs/mcs-api/issues
[work-api-issues]: https://github.com/kubernetes-sigs/work-api/issues
[implementations]: ../guides/index.md

## Communications

Major discussions and notifications will be sent on the [SIG-MC mailing
list][sigmcg].

We also have a [Slack channel (sig-multicluster)][slack] on k8s.io for day-to-day questions, discussions.

[sigmcg]: https://groups.google.com/forum/#!forum/kubernetes-sig-multicluster
[slack]: https://kubernetes.slack.com/archives/C09R1PJR3

## Meetings

Meetings discussing the evolution of the different APIs on SIG-Multicluster happen bi-weekly on Tuesdays at 9:30AM Pacific Time / 18:30 CET. Join kubernetes-sig-multicluster@googlegroups.com to get a calendar invite. 


<iframe
  src="https://calendar.google.com/calendar/u/0/embed?src=c5ac8984a64230b4c301124c52e53300440296806f61a22de507598a89c282ea@group.calendar.google.com&ctz=America/Los_Angeles"
  style="border: 0" width="800" height="600" frameborder="0"
  scrolling="no">
</iframe>

* [Zoom link](https://zoom.us/my/k8s.mc)
* [Convert to your timezone](http://www.thetimezoneconverter.com/?t=09:30&tz=PT%20%28Pacific%20Time%29)
* [Add to your calendar](https://calendar.google.com/calendar/u/0/r/eventedit/copy/MWlzc3MxZHIzbTM5Zmp0bWlxdDQwM2ZjcG5fMjAyMzAxMjRUMTczMDAwWiBjNWFjODk4NGE2NDIzMGI0YzMwMTEyNGM1MmU1MzMwMDQ0MDI5NjgwNmY2MWEyMmRlNTA3NTk4YTg5YzI4MmVhQGc)


### Meeting Notes and Recordings

Meeting agendas and notes are maintained in the [meeting notes
doc][meeting-notes]. Feel free to add topics for discussion at an upcoming
meeting.

All meetings are recorded and automatically uploaded to the [SIG Multicluster meetings Youtube playlist][sig-multicluster-yt-playlist].

#### Archived Notes
Some documents from previous quarters were uploaded [here][sig-mc-previous-quarters-docs].

[sig-mc-previous-quarters-docs]: https://drive.google.com/open?id=0B6O6mvmXbHiFRE03d0FPSGtTSG8

#### Initial Design Discussions


[sig-multicluster-yt-playlist]: https://www.youtube.com/playlist?list=PL69nYSiGNLP0HqgyqTby6HlDEz7i1mb0-
[sig-net-yt-playlist]: https://www.youtube.com/playlist?list=PL69nYSiGNLP2E8vmnqo5MwPOY25sDWIxb
[early-yt-playlist]: https://www.youtube.com/playlist?list=PL7KjrPTDcs4Xe6SZj-51WvBfufKf-la1O
[kubecon-2019-na-design-discussion]: https://docs.google.com/document/d/1l_SsVPLMBZ7lm_T4u7ZDBceTTUY71-iEQUPWeOdTAxM/preview
[kubecon-2019-eu-discussion]: https://docs.google.com/document/d/1n8AaDiPXyZHTosm1dscWhzpbcZklP3vd11fA6L6ajlY/preview
[sig-net-2019-11-sync]: https://docs.google.com/document/d/1AqBaxNX0uS0fb_fSpVL9c8TmaSP7RYkWO8U_SdJH67k/preview
[meeting-notes]: https://tinyurl.com/sig-multicluster-notes

## Presentations and Talks

[//]: # (Should we move this section in another tab or subtab? Maybe in the 'Reference' section or the 'Blog' section?)

| Date           | Title |    |
|----------------|-------|----|
| October, 2022 | [Kubecon NA 2022 Detroit: SIG Multicluster Intro & Deep Dive][2022-kubecon-na-schedule] (AWS-based demo combining About API and their MCS implementation with AWS CloudMap Controller)| [slides][2022-kubecon-na-slides], [video][2022-kubecon-na-video]|
| October, 2022 | [Kubecon NA 2022 Detroit: Multi-Cluster Stateful Set Migration: A solution to Upgrade Pain][2022-kubecon-na-mc-statefulset-schedule] | [slides][2022-kubecon-na-mc-statefulset-slides], [video][2022-kubecon-na-mc-statefulset-video] |
| May, 2022 | [Kubecon EU 2022 Valencia: SIG Multicluster Intro & Deep Dive][2022-kubecon-eu-schedule] (Demo on multicluster plugin for CoreDNS) | [video][2022-kubecon-eu-video] |
| October, 2021 | [Kubecon NA 2021 Los Angeles: SIG Multicluster Intro & Deep Dive][2021-kubecon-na-schedule]] (Explanation of MCS, multicluster DNS)| [slides][2021-kubecon-na-slides], [video][2021-kubecon-na-video] |
| October, 2021 | [Kubecon NA 2021 Los Angeles: Here Be Services: Beyond the Cluster Boundary with Multicluster Services][2021-kubecon-na-here-be-services-schedule] (Demo of MCS on GKE and Submariner.io) | [slides][2021-kubecon-na-here-be-services-slides], [video][2021-kubecon-na-here-be-services] |
| August, 2020 | [Kubecon EU 2020 Virtual : SIG Multicluster Intro][2020-kubecon-eu-schedule] | [video][2020-kubecon-eu-video] |
| November, 2019 | [Kubecon 2019 San Diego: Intro + Deep Dive SIG Multicluster][2019-kubecon-na-schedule] | [slides][2019-kubecon-na-community-slides] |
| May, 2019      | [Kubecon 2019 Barcelona: Ingress V2 and Multicluster Services][2019-kubecon-eu-ingress-v2] | [slides][2019-kubecon-eu-ingress-v2-slides], [video][2019-kubecon-eu-ingress-v2-video]|
| May, 2019      | [Kubecon 2019 Barcelona: Intro + Deep Dive: Multicluster SIG][2019-kubecon-eu-sig-mc-intro] | [video][2019-kubecon-eu-sig-mc-intro-video]


[2022-kubecon-na-schedule]: https://sched.co/182P2
[2022-kubecon-na-slides]: https://docs.google.com/presentation/d/106iQ-W3JiyWC_ek6EesisQWhg2bW4xfE514YFAQM3wo/edit?usp=sharing
[2022-kubecon-na-video]: https://www.youtube.com/watch?v=VZnF3YO1cm8

[2022-kubecon-na-mc-statefulset-schedule]: https://sched.co/182It
[2022-kubecon-na-mc-statefulset-video]: https://www.youtube.com/watch?v=hkyUqgwTZL8
[2022-kubecon-na-mc-statefulset-slides]: https://static.sched.com/hosted_files/kccncna2022/1c/KubeCon%20NA%2722_%20Multi-Cluster%20Stateful%20Set%20Migration_%20A%20Solution%20to%20Upgrade%20Pain.pptx.pdf

[2022-kubecon-eu-schedule]: https://sched.co/ytq6
[2022-kubecon-eu-video]: https://www.youtube.com/watch?v=cYFxjZEXucM

[2021-kubecon-na-schedule]: https://sched.co/lV6k
[2021-kubecon-na-slides]: https://static.sched.com/hosted_files/kccncna2021/d4/SIG%20Multicluster%20Intro%20%26%20Deep%20Dive%20KubeCon%20NA%202021-final.pdf

[2021-kubecon-na-video]: https://www.youtube.com/watch?v=zVTFm7HJD3s
[2021-kubecon-na-here-be-services-schedule]: https://sched.co/lV67
[2021-kubecon-na-here-be-services-slides]: https://static.sched.com/hosted_files/kccncna2021/5b/Here%20Be%20Services.pdf
[2021-kubecon-na-here-be-services]: https://www.youtube.com/watch?v=_UJrSfmvlMA

[2020-kubecon-eu-schedule]: https://sched.co/Zew0
[2020-kubecon-eu-video]: https://www.youtube.com/watch?v=bv9c1lJxDIo

[2019-kubecon-na-schedule]: https://sched.co/Uakw
[2019-kubecon-na-slides]: https://static.sched.com/hosted_files/kccncna19/29/SIG%20Multicluster%20KubeCon%20NA%202019%282%29.pdf

[2019-kubecon-na-video]: https://www.youtube.com/watch?v=cduG0FrjdJA

[2019-kubecon-eu-ingress-v2]: https://kccnceu19.sched.com/event/MPb6/ingress-v2-and-multicluster-services-rohit-ramkumar-bowei-du-google
[2019-kubecon-eu-ingress-v2-slides]: https://static.sched.com/hosted_files/kccnceu19/97/%5Bwith%20speaker%20notes%5D%20Kubecon%20EU%202019_%20Ingress%20V2%20%26%20Multi-Cluster%20Services.pdf
[2019-kubecon-eu-ingress-v2-video]: https://www.youtube.com/watch?v=Ne9UJL6irXY&t=1s

[2019-kubecon-eu-sig-mc-intro]: https://sched.co/MPlP
[2019-kubecon-eu-sig-mc-intro-video]: https://www.youtube.com/watch?v=GOiN1R2vQos

[2019-kubecon-na-community-slides]: https://docs.google.com/presentation/d/1s0scrQCCFLJMVjjGXGQHoV6_4OIZkaIGjwj4wpUUJ7M

## Code of conduct

Participation in the Kubernetes community is governed by the [Kubernetes Code of
Conduct](https://github.com/kubernetes/community/blob/master/code-of-conduct.md)
