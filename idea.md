ALEXIS: An Offline Sandbox Experience
=====================================

This main goal of this project is to build a caching system for remote resources that live on a sandbox ah abstract the syncing of those files.The application would be hosted on clients machine but would give the impression that it is on the sandbox.

Authentication
--------------
Users would authenticate to a sandbox by providing details:
- host: the sandbox host.
- username: the sandbox username
- password: the sandbox password

> The above details are available on the intranet

### Multi-Sandboxed Authentication

Users are allowed to login to different sandboxes but only one sandbox can be active per session.
The application also makes it easy to switch to a different sandbox without the user being required
to supply the information again. This process is called `sandbox switching`.

The cached files for different sandboxes are isolated from each other. So when the user switches
from sandbox A to sandbox B, the files that were cached from the sandbox A would no longer be
available in sandbox B until the user switches back to sandbox A.

File Caching
------------

Files would be fetched from the remote server using SFTP and would be synced at short intervals
that make it look like it's beign down in realtime.

When a command is sent to remote server,all cached files that are newer than the original are
synced with the original before the command is run.
After the command is run, if the contents of the original is newer that the cached version, the cache is updated.

Some of the caching would be done on disk to reduce memory consumption. File that are frequently modified would
be cached in memory to increase efficiency.
Cached files that aren't being used are discarded to reduced storage consumption.

Each cached file can have one of the following states:

1. modified
This is a state where the cached file has been modified by the user but has not been saved. This is a kind of checkpointed version.

2. staged
This is a state where the cached file has been saved by the user but has not been synced with the original.

3. synced
This is a state where the cached file has been synced with the original.

> A file versioning system is in place to keep track of different versions of the cached file, so users can easily roll back to previous versions if needed. A snapshot of the file is taken when the file is synced.

### caching algorithm

The **LRU** (_least reacently used_) caching algorithm would be implemented in the systems.
The LRU algorithm is based on the idea that items that have been accessed recently are more likely to be accessed again in the near future. The algorithm works by maintaining a linked list of items in the cache, where the most recently accessed item is at the head of the list and the least recently accessed item is at the tail. When a new item is added to the cache and the cache is full, the least recently accessed item at the tail of the list is evicted from the cache to make room for the new item.

Directory Structure Caching
---------------------------

The state of the current working directory is cached. The state is basically a datastructure showing the immediate contents of a directory (non-recursive) and their types (directories, files, symlinks...).


Error Handling
--------------

When network is disconnected, the user still has the ability to keep working on already cached files. The file would not go beyond the 'saved' state until the network connects and the file is synced.


Logging & Analytics
-------------------

The project implements:

1. A logging system that tracks all the actions performed on the application, including file access, file changes, and command execution, so that the administrator can easily monitor and troubleshoot any issues that may arise.
2. A analytics feature that tracks user activity and file usage which would help to optimize the system by identifying which type of files are most frequently accessed or modified.