# Automating CloudFront CNAME Migrations: A Zero-Downtime Approach Using Python

**Author:** Trevor Henning (hthennin)

## Overview

This Python automation script delivers a **zero-downtime approach** for CloudFront CNAME migrations by automatically updating DNS records the moment AWS Support completes a CNAME swap. Instead of manual coordination that leads to inevitable downtime, this solution continuously monitors your target CloudFront distribution and instantly updates Route 53 records when the migration occurs.

**Key Benefits:**
- ✅ **Zero-downtime migrations** - Eliminates the gap between CNAME swap and DNS updates
- ⚡ **Instant response** - Automated detection and DNS updates within seconds
- 🔄 **Continuous monitoring** - No manual timing coordination required
- 🛡️ **TLS protection** - Prevents certificate errors during transitions

## Problem Statement

When AWS Support performs a CNAME swap between CloudFront distributions, TLS connections break immediately after the swap until the customer updates their DNS record to point to the new distribution. This creates downtime that can be problematic for applications with strict uptime requirements.

## Zero-Downtime Solution

This **Python-powered automation** transforms manual CNAME migrations into seamless, zero-downtime operations:

1. **Real-time Monitoring** - Continuously polls the target CloudFront distribution for CNAME changes
2. **Instant Detection** - Identifies the moment AWS Support completes the CNAME swap
3. **Automated DNS Updates** - Immediately updates Route 53 records to point to the new distribution
4. **Downtime Elimination** - Reduces the traditional downtime window from minutes to mere seconds

## Prerequisites

- Python 3.x
- AWS SDK for Python (Boto3)
- Appropriate AWS credentials configured
- IAM permissions for CloudFront and Route 53 operations

## Installation

```bash
pip install boto3
```

## Usage

Run the script from the command line with the following parameters:

```bash
python3 cloudfront_dns_automation.py <new-distribution-id> <route53-hosted-zone-id> <old-cloudfront-domain> <new-cloudfront-domain> <alias-alternate-name>
```

### Example

```bash
python3 cloudfront_dns_automation.py EZDLMTR1D3MHD Z00646902JW6C5QG3Q2NG d2szizvz5rw5zj.cloudfront.net. d2mz62fpvuge8k.cloudfront.net. www.example.com
```

## Cross-Account Support

The script includes examples for assuming IAM roles when CloudFront distributions or Route 53 hosted zones are in different AWS accounts. Uncomment and modify the role assumption code as needed.

## Zero-Downtime Considerations

- **Maintenance Windows**: This automation enables CNAME swaps outside traditional maintenance windows by achieving near-zero downtime
- **DNS Propagation**: While the script eliminates coordination delays, global DNS propagation still takes 1-2 minutes
- **Continuous Operation**: The Python script runs continuously until the swap is detected, requiring no manual intervention
- **Production Ready**: Designed for high-availability applications with strict uptime requirements

## References

- [Moving an alternate domain name to a different distribution](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/alternate-domain-names-move.html#alternate-domain-names-move-options)
- [AWS IAM Role Switching](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html)

## Support

This script is provided as a reference implementation. Customers should test thoroughly in their environment and modify as needed for their specific use case.