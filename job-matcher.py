import google.generativeai as genai
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
load_dotenv()

# 1. Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# 2. Define Schema
class MatchResult(BaseModel):
    skills_match: float
    experience_match: float
    project_relevance: float
    overall_match: float
    matching_skills: list[str]
    missing_skills: list[str]
    explanation: str
candidate="""Vamshi Krishna 
Over all 6 + Years of experience in the IT Industry and having 5 + Years of experience in Azure, Configuration Management,
Infrastructure automation, and migration. Experience in dealing with Linux and Windows server administration. Working
experience on DevOps tools like Azure DevOps CI/CD and Terraform. Good Knowledge on Docker and Kubernetes.
Professional Summary:
 Experience on Azure infra and Azure DevOps based on client requirement.
 Hands-on Experience on Azure Cloud services (IaaS and PaaS) like networks, VM’s, Load balancers, Firewall, Microsoft
Entra, Storage account, Key Vault, Backups, Azure Log Analytics Workspace, Azure Monitor, Logic app, function app,
Webapp and Event Hubs etc.
 Designed Network Security Groups (NSGs) to control inbound and outbound access to network interfaces (NICs) and
subnets.
 Hands-on with storage accounts and with Blob, files and manage the SAS tokens and Keys.
 Having Experience in monitoring tools like Azure monitoring and Grafana.
 Led end-to-end Azure cloud migrations, assessing on-premises workloads using Azure Migrate, executing lift-and-shift
migrations via Azure Site Recovery (ASR), and optimizing costs post-migration with Reserved Instances and Auto-scaling.
 Modernized legacy applications by rehosting on Azure App Services/AKS and migrating databases to Azure SQL Managed
Instance, ensuring security compliance with Azure Policy and NSGs while minimizing downtime.
 Configuring the Azure Load Balancer, Application Gateway, and Experience Application Gateway (WAF) for Internet
based applications.
 Implementation and configuring of Azure backup and replications, troubleshooting on backup failures, replication issues.
 Experience on the Private endpoint and private links to route the traffic using Microsoft backbone network.
 Experience in setting up CI/CD pipeline to build and run Terraform/YAML jobs to create infrastructure in Azure
environment.
 Hands-on Experience in configuration of Service Principles, Self-hosted agents for Azure Devops Pipelines
 Experienced in Branching, Merging, Tagging, and maintaining the version across the environment using SCM tool
Git.
 Designed, developed, and maintained Terraform modules for provisioning and managing cloud infrastructure (AWS, Azure,
or GCP).
 Implemented modular and reusable Terraform code to standardize infrastructure deployments across environments (Dev,
QA, Prod).
 Used Terraform workspaces to manage multiple environments (e.g., staging, production) with a single codebase.
 Experience with Docker ACR for building and containerizing the multi-tier application to deploy.
 Experience working with Docker images with applications with its hardware and software dependencies.
 Publishing the docker images to Azure Container Registry (ACR) using with Azure Devops Pipelines.
 Hands on Kubernetes and managing containerized applications using its nodes, Config Map, Secretes, Services, Deployments,
and deployed application containers as pod.
 Good Knowledge on with and Kubernetes on AKS building and containerizing the application to deploy.
 Handled POC for AKS and ACR services using Docker and Kubernetes cluster services to manage local deployments in
Kubernetes by building a self-hosted Kubernetes cluster using CI/CD pipeline.
 Involved in container management using by writing Docker files and setting up the automated build on Docker HUB, installed
and configured Kubernetes.
Skills:
CI/CD: Azure Devops
Cloud Platform: Microsoft Azure IaaS/PaaS
IaC: Terraform
Container Technology: Docker and Kubernetes
Monitoring Tools: Azure Monitoring, Grafana, Prometheus
Configuration tool: Ansible
Build tools: Maven
Git/GitHub
OS: Windows/Linux
Artifact management: Artifactory, Blob storage
Scripting: Shell
Education:
 MCA from Jawaharlal Nehru Technological University, Hyderabad - 2010

Professional Experience:
1. Worked with Kumaran Systems, Fulltime (Bangalore)
Role: Cloud &amp; Devops Engineer
Client: CIBC
Duration: Apr 2024 to Jan 2025.
Roles and Responsibilities:
 Analyzing and understanding the client’s requirements and application functionalities.
 Creation of terraform modules
 Understanding existing CI/CD Yaml pipelines
 Writing terraforms scripts from scratch for building Dev, Test, Prod and DR environments
 Rehost / Lift and Shift – Used this Migration strategy for migrating applications from on premise to Azure platform
 Worked directly with Azure Product team in tracking and resolving defects in the Azure offerings
 Create Azure Infrastructure as a Service (IaaS) services like Virtual Networks, VMs, and Storage and monitoring the
resources through Azure Monitor.
 Creating VMs through Portal and Terraform code (IaC)
 Worked with Availability Sets, VM Scale sets.
 Experience in Virtual network setups, subnets, NICs, Public IPs.
 Configuring NSGs, used Network Watcher for troubleshooting.
 Creating Storage Accounts and provided SAS Access to the customers.
 Creating and Uploaded Blob files and worked with File shares.
 Preparing required documents for smoke test and migration acceptance testing (MAT)
 Demonstrates CD pipeline step up and working functionality to App Owner
 Doing Update or Close ADO tasks on timely manner.
 Configured and maintained Prometheus for metrics collection and alerting across cloud and on-premises infrastructure,
ensuring real-time monitoring and system reliability.
 Designed and implemented Grafana dashboards to visualize performance metrics, enabling proactive issue resolution and
improved operational visibility for DevOps.
2. Worked with UST Global, Fulltime (Hyderabad)
Role: Cloud Infrastructure Consultant
Client: Schroder’s Investment Management Limited
Duration: May 2022 to Jun 2023.
Roles and Responsibilities:
 Designed Network Security Groups (NSGs) to control inbound and outbound access to network interfaces (NICs) and
subnets.
 Hands-on with storage accounts and with Blob, files and manage the SAS tokens and Keys.
 Experience on the Azure key vault to store the secrets and certificates securely.
 Working Knowledge on RBAC policies, Roles, users and group and MFA authentication.
 Having Experience in monitoring tools like Azure monitoring and Grafana.
 Experienced in End-to-End cloud migration On-Premises to Azure cloud: Discovery, Assessment, Planning and
Migration.
 Configuring the Azure Load Balancer, Application Gateway, and Experience Application Gateway (WAF) for Internet
based applications.
 Implementation and configuring of Azure backup and replications, troubleshooting on backup failures, replication issues.
 Experience with High availability Sets, VM Scale sets.
 Experience on the Private endpoint and private links to route the traffic using Microsoft backbone network.
3. Worked with Cognizant, Fulltime (Hyderabad)
Role: Infrastructure Consultant
Client: Bayer –from Dec 2020 to Apr 2021.
Roles and Responsibilities:
 Analyzing and understanding the client’s requirements and application functionalities.
 Provided technical and functional recommendations based on project requirements.
 Responsible for design, implementation, architecture, and support for Azure Devops CI/CD pipelines
 Created Azure Landing zones for Australia east and ANZ region with zero touch deployment.
 Create and maintain highly scalable and fault tolerant multi-tier Azure environments across multiple availability zones using
terraform.
 Creation of terraform modules.
 Writing terraforms scripts from scratch for building Dev, Test, Prod and DR environments.
 Integrating Chekov tool to analyze terraform code.

 Worked in conjunction with multiple teams to make sure that the infrastructure and
 Customer applications work harmoniously together.
4. Worked with Krest Engineering &amp; Technology pvt ltd (Hyderabad)
Role: System Administrator
Client : Guru Gobind Singh Refinery
Duration: Jan 2017 to Nov 2019.
Roles and Responsibilities:
 Managed over 1800+ physical servers and 3500+ virtual machines across Hadoop, Azure, AWS, and VM environments,
ensuring optimal uptime and performance.
 Provisioned and maintained 200+ Azure VMs in DevTest environments and performed VM lifecycle operations across multi-
cloud platforms (Azure, AWS).
 Performed OS, kernel, firmware, and application upgrades, and configured BIOS and firmware updates using IMM &amp; ILO on
HP servers.
 Built/Upgraded OS, kernel, firmware, and Applications
 Handled disk and file system management, including LUN scanning, LVM configuration (PV, VG, LV), NFS setup, and
extending file systems based on application/database requirements
 Created and Maintained User accounts and group Administration, File system management.
 Created and managed user accounts, group policies, network configurations, and file servers (NFS, FTP), ensuring system-
level access and security controls.
 Automated tasks using CRON jobs and basic shell scripting
 Installed, removed, and upgraded new Packages using RPM and YUM.
 Monitored server performance (CPU, memory, disk thresholds), resolved incidents, joined SWAT calls for critical outages,
and managed backup operations using Avamar.
 Designed and implemented Azure networking components such as virtual networks and hybrid connectivity, with knowledge
of availability sets, fault domains, and update domains for high availability.
5. Worked with Anewa Engineering pvt ltd (Hyderabad)
Role: Junior System Administrator
Client: Universal Oil Products
Duration:Oct 2015 to Jan 2017.
Roles and Responsibilities:
 Managed installation, configuration, and maintenance of Windows Server environments (2012/2016/2019), including Active
Directory, DNS, and DHCP.
 Performed regular patch management, system updates, and server hardening to ensure compliance and security.
 Monitored server performance and resolved issues related to CPU, memory, disk space, and network connectivity.
 Implemented user and group policies using Group Policy Objects (GPOs) for access control and system configuration.
 Provided L1/L2 support for incident management, system troubleshooting, and root cause analysis to minimize downtime.
Certificates:
 Microsoft Azure Administrator Associate (AZ-104)
 Microsoft Designing and Implementing Microsoft DevOps Solutions (AZ-400)"""
# 3. Send Prompt
Job = """We are currently hiring for the position of JavaScript Backend Developer (Web Scraping) and are looking for experienced professionals who are strong in backend development using JavaScript technologies, particularly NestJS, ORM, and web scraping tools like Puppeteer.

Job Title: JavaScript Backend Developer
Experience: 6+ Years
Location: Hyderabad (Hybrid)

Type: Full-time

About the Role:
This role involves building and maintaining large-scale, data-heavy applications that process terabytes of data daily. You will be responsible for designing scalable backend solutions and working on real-time data processing, API development, and microservices architecture.

Key Responsibilities:

Design, develop, and test scalable backend systems
Build and maintain REST APIs and data processing workflows
Collaborate with internal and external teams for integration
Ensure performance, security, and fault tolerance
Troubleshoot and optimize for high-performance data handling
Required Skills:

Strong hands-on experience with JavaScript (Node.js)
Proficiency in NestJS, ORM, and Puppeteer
Good knowledge of PostgreSQL and database optimization
Experience with REST APIs, microservices, and message brokers
Familiarity with Agile/Scrum processes
Cloud experience (Azure preferred) but any other proven cloud experience req.
Strong understanding of design patterns and web sockets
Exposure to large-scale or big data applications is a plus
Qualifications:

Bachelor's or Master’s degree in Computer Science or related field
Minimum 6 years of relevant development experience 
"""
prompt = f"""
You are an AI that evaluates {candidate} profile against job requirements.
Return results STRICTLY in this JSON format:

{{
  "skills_match": number,
  "experience_match": number,
  "project_relevance": number,
  "overall_match": number,
  "matching_skills": [list of matched skills],
  "missing_skills": [list of missing skills],
  "explanation": "one-line explanation"
}}

Job desicription is{Job}:

make sure the be precise about the data in the json"""

response = model.generate_content(
    prompt,
    generation_config={"response_mime_type": "application/json"}
)

# 4. Parse JSON into Python object
result_pre = MatchResult.model_validate_json( response.text)
result=result_pre.model_dump_json(indent=8)
print(result)
