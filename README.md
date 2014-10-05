APRINTICE
=========

APRINTICE is a "pull-printing" service. It is a centralized printing server that
manages queues, quotas, and balances for users in an organization. Users may
print documents to the queue, and then release them at a printing kiosk or on
the web, while keeping track of their balance.

This project aims to be a free, open source solution to similar services which
can be prohibitively expensive to smaller organizations such as libraries. The
service runs on a Linux server, and is compatible with Windows, Mac, and Linux
clients.

Unlike other implementations, APRINTICE uses an open source library to
approximate the ink usage of documents, and can adjust the cost accordingly.
Multiple printers are supported, and each may have its own associated costs.

At the core of the service is a CUPS server that exposes a virtual printer which
accepts jobs and stores them on disk until released. A web service, using
Python, the Pyramid application framework, HTML5, CSS3, jQuery, and AngularJS,
allows users to log in and manage their pending jobs.
