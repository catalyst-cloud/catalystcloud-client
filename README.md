# Catalyst Cloud API client

[![PyPI](https://img.shields.io/pypi/v/catalystcloud-client)](https://pypi.org/project/catalystcloud-client) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/catalystcloud-client) [![GitHub](https://img.shields.io/github/license/catalyst-cloud/catalystcloud-client)](https://github.com/catalyst-cloud/catalystcloud-client/blob/main/LICENSE) ![Test Status](https://img.shields.io/github/actions/workflow/status/catalyst-cloud/catalystcloud-client/test.yml?label=tests)

This is a package for installing the API clients and all necessary
plugins for interacting with [Catalyst Cloud](https://catalystcloud.nz).

Catalyst Cloud is an [OpenStack](https://openstack.org)-based public cloud,
with data centres across New Zealand. We provide a range of different services
for our customers, and have created this package to make it easier
for customers to create a CLI environment from which they can interact
with our cloud.

Note that this library is not required to interact with Catalyst Cloud APIs.
The individual client libraries can be installed and used separately from
this package; for more information refer to [Available Commands](#available-commands).

## Installation

The Catalyst Cloud API client supports Python 3.8 and later,
and is supported for Linux, macOS and Windows clients.

### pipx

The recommended installation method is to use [`pipx`](https://pipx.pypa.io).
This installs the [`catalystcloud-client`](https://pypi.org/project/catalystcloud-client)
package into an isolated virtual environment, while also making the installed commands
available for your local user.

```bash
pipx install catalystcloud-client --include-deps
```

> [!NOTE]
> The `--include-deps` option is required to expose the `openstack` command
> used to interact with Catalyst Cloud.

### pip

The Catalyst Cloud API client can also be installed directly using `pip`.
This is useful when installing the package in a container image build,
for example.

```bash
python -m pip install catalystcloud-client
```

This exposes the `openstack` command used to interact with Catalyst Cloud
in the running Python environment.

> [!WARNING]
> When installing using `pip` it is highly recommended to install the API client
> into a virtual environment.
>
> This ensures that there are no conflicts with packages installed into the
> Python environment managed by your operating system.

## Usage

For more information on how to interact with Catalyst Cloud from a command line
environment, please refer to [CLI Tools and SDKs](https://docs.catalystcloud.nz/sdks-and-toolkits.html)
in the Catalyst Cloud documentation.

## Available Commands

Installing the Catalyst Cloud API client makes the following commands available:

* `openstack` - The OpenStack API client. Used for most tasks via sub-commands.
* `swift` - The Swift API client. An alternative command for interacting with
  the [Catalyst Cloud Object Storage](https://docs.catalystcloud.nz/object-storage.html)
  service using the Swift API.

Using the `openstack` command, the following services can be managed:

| Service        | Resource Type           | Sub-command                        | API Client Library      |
|----------------|-------------------------|------------------------------------|-------------------------|
| Identity       | Projects                | `openstack project`                | `python-keystoneclient` |
| Identity       | Users                   | `openstack user`                   | `python-keystoneclient` |
| Identity       | EC2 Credentials         | `openstack ec2 credentials`        | `python-keystoneclient` |
| Identity       | Application Credentials | `openstack application credential` | `python-keystoneclient` |
| Compute        | Instances / Servers     | `openstack server`                 | `python-novaclient`     |
| Compute        | Keypairs                | `openstack keypair`                | `python-novaclient`     |
| Networking     | Networks                | `openstack network`                | `python-neutronclient`  |
| Networking     | Routers                 | `openstack router`                 | `python-neutronclient`  |
| Networking     | Floating IPs            | `openstack floating ip`            | `python-neutronclient`  |
| Networking     | Security Groups         | `openstack security group`         | `python-neutronclient`  |
| Networking     | VPNs                    | `openstack vpn`                    | `python-neutronclient`  |
| Load Balancer  | Load Balancers          | `openstack loadbalancer`           | `python-octaviaclient`  |
| Block Storage  | Volumes                 | `openstack volume`                 | `python-cinderclient`   |
| Image          | Images                  | `openstack image`                  | `python-glanceclient`   |
| Database       | Databases               | `openstack database`               | `python-troveclient`    |
| Orchestration  | Stacks                  | `openstack stack`                  | `python-heatclient`     |
| Kubernetes     | Clusters                | `openstack coe cluster`            | `python-magnumclient`   |
| Kubernetes     | Node Groups             | `openstack coe nodegroup`          | `python-magnumclient`   |
| Object Storage | Containers              | `openstack container`              | `python-swiftclient`    |
| Object Storage | Objects                 | `openstack object`                 | `python-swiftclient`    |
| Object Storage | Accounts                | `openstack object store account`   | `python-swiftclient`    |
| Telemetry      | Metrics                 | `openstack metric`                 | `gnocchiclient`         |
| Telemetry      | Alarms                  | `openstack alarm`                  | `aodhclient`            |
| Billing        | Invoices                | `openstack rating invoice`         | `python-distilclient`   |
| Billing        | Quotations              | `openstack rating quotation`       | `python-distilclient`   |
| Billing        | Products                | `openstack rating product`         | `python-distilclient`   |
| Administration | Project Users           | `openstack project user`           | `python-adjutantclient` |
| Administration | Project Quotas          | `openstack project quota`          | `python-adjutantclient` |
| Administration | Manageable Roles        | `openstack manageable roles`       | `python-adjutantclient` |
| Administration | Passwords               | `openstack password`               | `python-adjutantclient` |

For more information on using these services, please refer to the
[Catalyst Cloud documentation](https://docs.catalystcloud.nz).