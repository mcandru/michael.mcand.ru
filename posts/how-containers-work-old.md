---
title: How Containers Actually Work
date: 2026-03-28
---

A common explanation of a container is that it’s basically a lightweight virtual machine. This is certainly a reasonable starting point, but for me it raises a question: lightweight _how exactly_? What has been removed from a VM and what has been kept? And what does a container actually look like from the operating system’s perspective? I’m going to give a go to spelling out a little more about how containers actually work under the hood.

**Disclaimer: this post won’t teach you how to use Docker. This is not a Docker how-to guide.**

<img src="/img/how-containers-work/vm-vs-container.png" style="width: 100%" />

_At a high level, a container will always run on the host OS whereas a VM virtualises at the hardware level._

## Containers Are Just Processes

From the operating system perspective, containers are just processes. In OS terms, a **program** is a static executable file stored on disk that contains instructions for a computer to perform tasks, and a **process** is an executing instance of a program.

A process includes the program code, and data. The host OS is responsible for scheduling processes to be run on the CPU.

Let’s take a look at a simple example. Let’s try to run an NGINX web server container with Docker:

```bash
~$ docker run -d --name web-server nginx
```

We can use the `docker top` command to get a list of the running processes for that container:

```bash
~$ sudo docker top web-server
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                200800              200776              0                   11:32               ?                   00:00:00            nginx: master process nginx -g daemon off;
message+            200841              200800              0                   11:32               ?                   00:00:00            nginx: worker process
```

In this case, starting the NGINX container created two processes, a master process for the web server and a worker process that can be used to handle requests. We can also validate that these are just regular old processes running on the system with `ps` to list the running processes:

```bash
~$ ps aux | grep nginx
root      200800  0.0  1.9  14860  8916 ?        Ss   11:32   0:00 nginx: master process nginx -g daemon off;
message+  200841  0.0  0.7  15316  3704 ?        S    11:32   0:00 nginx: worker process
```

## Containers Are Isolated Processes

Containers have three main requirements worth mentioning:

1. **Isolation** - containers should run in a sandboxed environment with its own filesystem, processes, and networking, and mitigate any risks of an application interfering with the rest of the OS.
2. **Resource Control** - the container should be limited in how much CPU, memory, and I/O it can consume, preventing any single container from starving others sharing the same host.
3. **Portability** - containers should be able to package everything needed to run an application, including all of its dependencies, into a single snapshot of files and directories that can be run on nearly any system

By default on Linux, processes are somewhat isolated. A process cannot access the memory space of any other process running on the OS. This is important to prevent running processes from causing other processes to crash, and to ensure that a malicious process can’t steal sensitive data from its contemporaries.

However, processes still have a view of the system that they are running on. They can see the full filesystem, they can see metadata about each other, and they share the same network stack.

For example, the following Python program prints all files in the current working directory and lists the PIDs of all active processes on the OS:

```python
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "psutil>=7.2.2",
# ]
# ///

import os
import psutil

print("Current directory:")
for f in os.listdir():
    print(f"- {f}")

print("Process list:")
for p in psutil.process_iter(["pid"]):
    print(p.info["pid"])
```

The output of this program should look something like:

```python
~$ uv run process.py
Current directory:
- process.py
- test.txt
Process list:
0
1
177
17
...
```

So plain processes fall short on all four goals: they share the host's filesystem, network stack, and process tree, breaking **isolation,** they have no built-in limits on CPU or memory usage, breaking **resource control,** and they depend on whatever libraries and dependencies happen to be installed on the host, breaking **portability**. Let’s next take a closer look at how Docker’s container implementation solves these issues.

### 1. Isolation - Namespaces

It turns out that there exists a neat feature in the Linux kernel called **namespaces** that partition kernel resources. A namespace defines what kernel resources can be viewed, and a process that uses the namespace can only see these resources. Isolation can be securely implemented using namespaces because the OS kernel controls what kernel-level operations all processes can perform.

There are many different types of namespaces, some types that are of interest to containers are:

- **PID namespace:** the process gets its own process tree. It can only see processes in its own namespace. Its first process becomes PID 1.
- **Network namespace:** the process gets its own network stack, its own interfaces, its own routing table, its own ports
- **Mount namespace:** the process gets its own view of the filesystem
- **UTS namespace:** the process gets its own hostname
- **Inter-process Communication (IPC) namespace:** the process gets its own inter-process communication resources, such as message queues, semaphores, and shared memory segments. Processes in different IPC namespaces cannot communicate through these mechanisms
- **User namespace:** the process gets its own mapping of user and group IDs. This means that a process can appear to run as root (UID 0) inside the namespace while mapping to an unprivileged user on the host which is useful for security

<img src="/img/how-containers-work/namespace-isolation.png" style="width: 100%" />

By default, every Linux system has one namespace for each type and every forked process uses the namespace of their parent, and by default processes are created with the default namespace. However, you can create namespaces to control resource access for each. When Docker creates a new container, it typically creates a new namespace of each type specifically for all container processes in order to achieve the level of observed process isolation.

To show that container processes achieve this level of isolation, let’s _dockerise_ the Python `process.py` example from earlier:

```docker
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY process.py /app/process.py

WORKDIR /app
CMD ["uv", "run", "process.py"]
```

You can build and run this with:

```bash
$ docker build --tag docker-python-process .
$ docker run docker-python-process
```

This will run the same `process.py` Python script as before, but inside a Docker container.

```bash
Current directory:
- process.py
Process list:
1
33
```

You will notice that the files in the file system are completely different from when we run the script natively. There are also a much smaller number of process PIDs printed. The container process doesn’t have the same view of the filesystem and processes because it is running in a constrained mount and PID namespace.

### 2. Resource Control - Cgroups

One important component of containers is the ability to isolate the usage of resources like the CPU, memory, and disk I/O. This can be useful to prevent a container from hogging all of the resources on a machine.

To implement this functionality, Docker leans on another Linux kernel feature called **cgroups**. Google developed cgroups in the early 2000’s to manage their massive internal infrastructure management system, Borg, to be able for different applications to share the same hardware efficiently without interfering with each other. It added the ability to control resource usage by a process by creating a group that defined the usage constraints of all processes in the group. Processes could then join the group and the kernel would enforce these constraints.

When you run a docker command like:

```python
$ docker run --memory=512m --cpus=1 -d --name web-server nginx
```

a container will be created with CPU and Memory cgroups configured to limit usage.

Cgroups are actually exposed as a virtual filesystem in Linux, so you can browse them like regular files:

```bash
~$ ls /sys/fs/cgroup/
cgroup.controllers      cgroup.stat             cpu.stat.local         dev-mqueue.mount  io.prio.class     memory.stat                    sys-fs-fuse-connections.mount  user.slice
cgroup.max.depth        cgroup.subtree_control  cpuset.cpus.effective  init.scope        io.stat           memory.zswap.writeback         sys-kernel-config.mount
cgroup.max.descendants  cgroup.threads          cpuset.cpus.isolated   io.cost.model     memory.numa_stat  misc.capacity                  sys-kernel-debug.mount
cgroup.pressure         cpu.pressure            cpuset.mems.effective  io.cost.qos       memory.pressure   misc.current                   sys-kernel-tracing.mount
cgroup.procs            cpu.stat                dev-hugepages.mount    io.pressure       memory.reclaim    proc-sys-fs-binfmt_misc.mount  system.slice
```

You can take a look a container’s cgroup with:

```bash
~$ cat /proc/$(sudo docker inspect --format '{{.State.Pid}}' web-server)/cgroup
0::/system.slice/docker-2c53af8539092141978bb91a17fe06a2093e30ad32ba4930c4ccfd3bb7591423.scope
```

and then use it to read specific limits set by the cgroup:

```bash
~$ cat /sys/fs/cgroup/system.slice/docker-2c53af8539092141978bb91a17fe06a2093e30ad32ba4930c4ccfd3bb7591423.scope/memory.max
536870912
```

To understand a little bit more about _how_ the OS limits resource usage, we have to understand a little bit about how processes use resources. When a process needs a resource, say memory as an example, it sends a syscall to the OS requesting memory. The kernel memory allocator then allocates the memory, and returns information about the resulting memory allocation back to the process. The kernel can check if a process belongs to a cgroup, and if so, checks whether the memory allocation would exceed any limits defined in the cgroup. I won’t go into the details of how cgroups limit other resources but you get the idea[1].

<img src="/img/how-containers-work/cgroup-resource-limiting.png" style="width: 100%" />

### 3. Portability - Images

So if a container is simply a group of isolated processes running in an environment with their own cgroup, how is the portability goal of containers implemented? A large part of the usefulness of containers comes from the ability to package up entire applications and all of their resources into a single bundle that can be run anywhere.

That’s where container images come in. A container image is a standard package that includes all of the files, binaries, libraries, and config required to run a container. When a container mount namespace is created and pointed to a directory on disk, everything in the image is copied into that directory. A container process can then access everything in the image.

One thing that confused me when I started using Docker is that I can create a “Ubuntu” container and shell into it with a command like:

```bash
~$ docker run -it ubuntu:latest bash
root@c6cdec8d7646:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

I will get a shell with a directory structure that looks awfully like Ubuntu. I can even apt install and use packages, even if I’m not running Ubuntu as my host OS:

```bash
root@c6cdec8d7646:/# apt install curl
```

So what’s happening here exactly? We fetched the official [Ubuntu Docker image from DockerHub](https://hub.docker.com/_/ubuntu) and spun up a container to run it. But this isn’t the full Ubuntu OS, it’s just the root directory (`/`) of the OS, containing the filesystem, libraries and tools that Ubuntu ships with.

This bundles in the `bash` program that allows us to shell into the container like we would on any OS, and the `apt` program that lets us install any executable from the apt repository. However, every executable in the Ubuntu image is run on the host OS, not on a Ubuntu kernel.

So even though the running container from the Ubuntu image _feels_ a lot like Ubuntu, it’s not quite. The reason why this is useful is so that we can bundle absolutely every possible dependency that we may need in the container. If the application needs to use some OS utilities, we need to bundle those into the container.

#### Layers

But it’s quite rare that we wish to containerise just the Ubuntu user space. Typically, we will want to add files, config, and binaries that we need to actually run our application too. Docker allows us to define changes to an image using a `Dockerfile` :

```docker
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY process.py /app/process.py

WORKDIR /app
CMD ["uv", "run", "process.py"]
```

The `FROM` command allows us to import some kind of a base image that has a bunch of files, and utilities that we might need already included. Every line in the `Dockerfile` is called a **layer**. Each layer can essentially be thought of as a set of file system changes that could add, remove, or modify files in the image. When you have defined a `Dockerfile`, the image has to be built from it. This is just the process of reading and executing each layer defined in the `Dockerfile` and saving the resulting snapshot.

One very neat thing about this layered approach to building images is that, because they build on top of each other sequentially, they can be cached. If you make a change to a `Dockerfile`, you will only have to rebuild the image from the line that you changed and down, as the state of the image will be unchanged from before that point.

<img src="/img/how-containers-work/image-layers.png" style="width: 100%" />

## Creating an Isolated Process from Scratch

At this point we now know that containers are just processes that are magically isolated and resource controlled thanks to a few Linux OS features, and that we can bundle an image and copy it into the root directory of a process.

We can now put all of this knowledge together to build a very basic container runtime. I have built a container runtime in ~300 lines of Python that I have called `pycrate`. You can clone the repo and try it for yourself here:

[https://github.com/mcandru/pycrate](https://github.com/mcandru/pycrate)

I built it in Python for educational purposes as Python is more widely readable than C. The implementation is also full of security holes but I think that it’s still useful to see the vibe of something that resembles a container runtime, and that it’s not just magic.

You can run a “container” by running:

```bash
~$ sudo ./pycrate.py run ubuntu.tar.gz /bin/bash
```

and you will get a Ubuntu-like shell experience.

At its core, the way it works is relatively straightforward:

1. **Extract the image** - for example if you specify `ubuntu.tar.gz`, we need to uncompress it and then copy it to a temporary directory that we’ll use as the root directory for the container
2. **Set up cgroups** - You can specify `--memory` and `--cpu` arguments to the command. If you do, we create a new directory in the `/sys/fs/cgroup` directory. This is a virtual filesystem in which the kernel will intercept the `mkdir` and automatically populate it with all of the control interface files needed for a cgroup. We then make changes to the `memory.max` and `cpu.max` files as needed to specify the limitations
3. **Create namespaces** - we create a new PID, mount, hostname, network, and IPC namespace to isolate the process. This will apply to the current process and any child processes that it creates
4. **Fork the process** - After creating the namespaces, we fork the process. Forking is a bit funky when you first see it, it is essentially creating an exact copy of a process from the current point of execution of the program code. The forked child is now the container.
5. **Set up the filesystem** - once we have forked the process, we need to set up the filesystem. By default, when we fork the process, we can still see the old `/proc` directory that contains file descriptors for all OS processes, but we shouldn’t be able to access them. We can remount the `/proc` directory to view the new PIDs only viewable by the child process. We also need to set the new root directory for the child process. In my example code we use `chroot`, but this has a pretty gnarly escape where you can get access to the real root folder of the system. This is because `chroot` only changes the current process’s notion of the root directory. You can simply `chroot` again to another relative path and break out. There are other ways to **change the mount tree root directory itself** but I chose not to use it for this example project to try to keep the code as simple and understandable as possible.

And there we have it, a poor mans container runtime, complete with no network access, incomplete isolation, and at least one major security vulnerability. The concepts are simple, but the implementation is not so much. However, it was still a fun educational exercise, especially as someone who is not familiar with low-level kernel interfaces.

## Conclusion

Containers aren't magic, although using them can make it feel like they are. They're processes with a few clever tricks added on: **namespaces** to limit what the process can see, **cgroups** to limit what it can consume, and **images** to bundle everything it needs into a portable snapshot.

I hope this post demystifies the black box a little. The next time you run `docker run`, you'll know that somewhere under the hood, the kernel is creating some isolated processes, giving it a restricted view of its world, and pointing it at a directory full of files.

## Footnotes

[1] You may at this point be thinking, if Docker containers rely on namespaces and cgroups in Linux to isolate processes, how do they work on macOS or Windows? Well the short answer is that they don’t. When you run Docker on Mac or Windows it actually runs in a lightweight, purpose-built Linux VM. In theory any performance hit from running containers in the VM should be minimal, but in practice it is relatively well accepted that running Docker on Linux has meaningful performance benefits.
