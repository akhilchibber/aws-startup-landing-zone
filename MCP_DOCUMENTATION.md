# Kiro MCP (Model Context Protocol) Documentation

This document provides a comprehensive overview of all available MCPs in Kiro, their functionality, and the tools they provide.

---

## Table of Contents

1. [Supabase MCP](#supabase-mcp)
2. [Playwright MCP](#playwright-mcp)
3. [GitHub MCP](#github-mcp)
4. [Vercel MCP](#vercel-mcp)
5. [AWS Documentation MCP](#aws-documentation-mcp)
6. [AWS API MCP](#aws-api-mcp)
7. [Netlify MCP](#netlify-mcp)
8. [AWS Diagram MCP](#aws-diagram-mcp)
9. [Terraform MCP](#terraform-mcp)
10. [AWS Terraform MCP](#aws-terraform-mcp)

---

## Supabase MCP

**Status:** Enabled  
**URL:** https://mcp.supabase.com/mcp

### Functionality
The Supabase MCP provides tools for managing Supabase projects, databases, and backend services. It enables interaction with Supabase's PostgreSQL database, authentication, real-time features, and storage.

### Available Tools

#### Organization Management
- `mcp_supabase_list_organizations` - List all organizations the user is a member of
- `mcp_supabase_get_organization` - Get details for a specific organization (includes subscription plan)

#### Project Management
- `mcp_supabase_list_projects` - List all Supabase projects for the user
- `mcp_supabase_get_project` - Get details for a specific Supabase project
- `mcp_supabase_pause_project` - Pause a Supabase project
- `mcp_supabase_restore_project` - Restore a paused Supabase project
- `mcp_supabase_create_project` - Create a new Supabase project
- `mcp_supabase_get_cost` - Get the cost of creating a new project or branch
- `mcp_supabase_confirm_cost` - Confirm cost before creating a project or branch

#### Database Operations
- `mcp_supabase_list_tables` - List all tables in one or more schemas
- `mcp_supabase_list_extensions` - List all extensions in the database
- `mcp_supabase_list_migrations` - List all migrations in the database
- `mcp_supabase_apply_migration` - Apply a migration to the database (DDL operations)
- `mcp_supabase_execute_sql` - Execute raw SQL in the Postgres database

#### API & Keys
- `mcp_supabase_get_project_url` - Get the API URL for a project
- `mcp_supabase_get_publishable_keys` - Get all publishable API keys for a project

#### Type Generation
- `mcp_supabase_generate_typescript_types` - Generate TypeScript types for a project

#### Edge Functions
- `mcp_supabase_list_edge_functions` - List all Edge Functions in a project
- `mcp_supabase_get_edge_function` - Retrieve file contents for an Edge Function
- `mcp_supabase_deploy_edge_function` - Deploy an Edge Function to a project

#### Branching
- `mcp_supabase_create_branch` - Create a development branch on a project
- `mcp_supabase_list_branches` - List all development branches of a project
- `mcp_supabase_delete_branch` - Delete a development branch
- `mcp_supabase_merge_branch` - Merge migrations and edge functions from a branch to production
- `mcp_supabase_reset_branch` - Reset migrations of a development branch
- `mcp_supabase_rebase_branch` - Rebase a development branch on production

#### Monitoring & Diagnostics
- `mcp_supabase_get_logs` - Get logs for a project by service type (API, Postgres, Edge Functions, Auth, Storage, Realtime)
- `mcp_supabase_get_advisors` - Get advisory notices for security vulnerabilities or performance improvements

---

## Playwright MCP

**Status:** Enabled  
**Command:** npx @playwright/mcp@latest

### Functionality
The Playwright MCP provides tools for browser automation and web testing. It enables automated interaction with web pages, taking screenshots, filling forms, and performing various browser operations.

### Available Tools

#### Navigation & Page Management
- `mcp_playwright_browser_navigate` - Navigate to a URL
- `mcp_playwright_browser_navigate_back` - Go back to the previous page in history
- `mcp_playwright_browser_close` - Close the page
- `mcp_playwright_browser_tabs` - List, create, close, or select browser tabs
- `mcp_playwright_browser_install` - Install the browser specified in config

#### Interaction
- `mcp_playwright_browser_click` - Perform click on a web page (left, right, middle button)
- `mcp_playwright_browser_type` - Type text into editable element
- `mcp_playwright_browser_fill_form` - Fill multiple form fields at once
- `mcp_playwright_browser_select_option` - Select an option in a dropdown
- `mcp_playwright_browser_hover` - Hover over element on page
- `mcp_playwright_browser_drag` - Perform drag and drop between two elements
- `mcp_playwright_browser_press_key` - Press a key on the keyboard
- `mcp_playwright_browser_file_upload` - Upload one or multiple files

#### Inspection & Snapshots
- `mcp_playwright_browser_snapshot` - Capture accessibility snapshot of the current page
- `mcp_playwright_browser_take_screenshot` - Take a screenshot of the current page
- `mcp_playwright_browser_evaluate` - Evaluate JavaScript expression on page or element

#### Monitoring
- `mcp_playwright_browser_console_messages` - Returns all console messages
- `mcp_playwright_browser_network_requests` - Returns all network requests since loading the page
- `mcp_playwright_browser_wait_for` - Wait for text to appear/disappear or a specified time to pass

#### Advanced
- `mcp_playwright_browser_handle_dialog` - Handle a dialog (alert, confirm, prompt)
- `mcp_playwright_browser_resize` - Resize the browser window
- `mcp_playwright_browser_run_code` - Run Playwright code snippet

---

## GitHub MCP

**Status:** Enabled  
**Command:** npx -y @modelcontextprotocol/server-github  
**Auto-Approved Tools:** get_file_contents

### Functionality
The GitHub MCP provides tools for interacting with GitHub repositories, managing issues, pull requests, and repository content. It enables automation of GitHub workflows and repository management.

### Available Tools

#### Repository Management
- `mcp_github_create_repository` - Create a new GitHub repository in your account
- `mcp_github_search_repositories` - Search for GitHub repositories
- `mcp_github_fork_repository` - Fork a GitHub repository to your account or organization

#### File Operations
- `mcp_github_get_file_contents` - Get the contents of a file or directory from a repository
- `mcp_github_create_or_update_file` - Create or update a single file in a repository
- `mcp_github_push_files` - Push multiple files to a repository in a single commit

#### Branch Management
- `mcp_github_create_branch` - Create a new branch in a repository
- `mcp_github_list_commits` - Get list of commits of a branch

#### Issue Management
- `mcp_github_create_issue` - Create a new issue in a repository
- `mcp_github_list_issues` - List issues in a repository with filtering options
- `mcp_github_get_issue` - Get details of a specific issue
- `mcp_github_update_issue` - Update an existing issue
- `mcp_github_add_issue_comment` - Add a comment to an existing issue

#### Pull Request Management
- `mcp_github_create_pull_request` - Create a new pull request
- `mcp_github_list_pull_requests` - List and filter repository pull requests
- `mcp_github_get_pull_request` - Get details of a specific pull request
- `mcp_github_get_pull_request_files` - Get the list of files changed in a pull request
- `mcp_github_get_pull_request_status` - Get the combined status of all status checks for a PR
- `mcp_github_get_pull_request_comments` - Get the review comments on a pull request
- `mcp_github_get_pull_request_reviews` - Get the reviews on a pull request
- `mcp_github_create_pull_request_review` - Create a review on a pull request
- `mcp_github_merge_pull_request` - Merge a pull request
- `mcp_github_update_pull_request_branch` - Update a pull request branch with latest changes

#### Search
- `mcp_github_search_code` - Search for code across GitHub repositories
- `mcp_github_search_issues` - Search for issues and pull requests across repositories
- `mcp_github_search_users` - Search for users on GitHub

---

## Vercel MCP

**Status:** Enabled  
**Command:** npx -y @open-mcp/vercel  
**Auto-Approved Tools:** getprojects, createproject, getproject, getdeployments, createdeployment, getdeployment

### Functionality
The Vercel MCP provides tools for managing Vercel projects, deployments, domains, and infrastructure. It enables deployment automation, project configuration, and environment management.

### Available Tools

#### Project Management
- `mcp_vercel_getprojects` - Retrieve a list of projects
- `mcp_vercel_createproject` - Create a new project
- `mcp_vercel_getproject` - Find a project by id or name
- `mcp_vercel_updateproject` - Update an existing project
- `mcp_vercel_deleteproject` - Delete a project
- `mcp_vercel_pauseproject` - Pause a project
- `mcp_vercel_unpauseproject` - Unpause a project

#### Deployment Management
- `mcp_vercel_getdeployments` - List deployments
- `mcp_vercel_createdeployment` - Create a new deployment
- `mcp_vercel_getdeployment` - Get a deployment by ID or URL
- `mcp_vercel_canceldeployment` - Cancel a deployment
- `mcp_vercel_deletedeployment` - Delete a deployment
- `mcp_vercel_getdeploymentevents` - Get deployment events
- `mcp_vercel_getdeploymentfilecontents` - Get deployment file contents
- `mcp_vercel_listdeploymentfiles` - List deployment files

#### Domain Management
- `mcp_vercel_getdomains` - List all domains
- `mcp_vercel_getdomain` - Get information for a single domain
- `mcp_vercel_getdomainconfig` - Get a domain's configuration
- `mcp_vercel_checkdomainstatus` - Check domain availability
- `mcp_vercel_checkdomainprice` - Check the price for a domain
- `mcp_vercel_buydomain` - Purchase a domain
- `mcp_vercel_deletedomain` - Remove a domain by name
- `mcp_vercel_patchdomain` - Update or move apex domain
- `mcp_vercel_getdomaintransfer` - Get domain transfer info

#### DNS Records
- `mcp_vercel_getrecords` - List existing DNS records
- `mcp_vercel_createrecord` - Create a DNS record
- `mcp_vercel_updaterecord` - Update an existing DNS record
- `mcp_vercel_removerecord` - Delete a DNS record

#### Project Domains
- `mcp_vercel_getprojectdomains` - Retrieve project domains by project
- `mcp_vercel_getprojectdomain` - Get a project domain
- `mcp_vercel_addprojectdomain` - Add a domain to a project
- `mcp_vercel_updateprojectdomain` - Update a project domain
- `mcp_vercel_removeprojectdomain` - Remove a domain from a project
- `mcp_vercel_moveprojectdomain` - Move a project domain
- `mcp_vercel_verifyprojectdomain` - Verify project domain

#### Environment Variables
- `mcp_vercel_filterprojectenvs` - Retrieve environment variables of a project
- `mcp_vercel_createprojectenv` - Create one or more environment variables
- `mcp_vercel_getprojectenv` - Retrieve the decrypted value of an environment variable
- `mcp_vercel_editprojectenv` - Edit an environment variable
- `mcp_vercel_removeprojectenv` - Remove an environment variable

#### Team Management
- `mcp_vercel_getteams` - List all teams
- `mcp_vercel_getteam` - Get a team
- `mcp_vercel_createteam` - Create a team
- `mcp_vercel_patchteam` - Update a team
- `mcp_vercel_deleteteam` - Delete a team
- `mcp_vercel_getteammembers` - List team members
- `mcp_vercel_inviteusertoteam` - Invite a user to a team
- `mcp_vercel_updateteammember` - Update a team member
- `mcp_vercel_removeteammember` - Remove a team member
- `mcp_vercel_requestaccesstoteam` - Request access to a team
- `mcp_vercel_jointeam` - Join a team
- `mcp_vercel_getteamaccessrequest` - Get access request status
- `mcp_vercel_deleteteaminvitecode` - Delete a team invite code

#### Project Members
- `mcp_vercel_getprojectmembers` - List project members
- `mcp_vercel_addprojectmember` - Add a new member to a project
- `mcp_vercel_removeprojectmember` - Remove a project member

#### Aliases
- `mcp_vercel_listaliases` - List aliases
- `mcp_vercel_getalias` - Get an alias
- `mcp_vercel_listdeploymentaliases` - List deployment aliases
- `mcp_vercel_assignalias` - Assign an alias
- `mcp_vercel_deletealias` - Delete an alias

#### Webhooks
- `mcp_vercel_createwebhook` - Create a webhook
- `mcp_vercel_getwebhooks` - Get a list of webhooks
- `mcp_vercel_getwebhook` - Get a webhook
- `mcp_vercel_deletewebhook` - Delete a webhook

#### Certificates
- `mcp_vercel_get_certs` - Get certificates
- `mcp_vercel_getcertbyid` - Get cert by id
- `mcp_vercel_issuecert` - Issue a new cert
- `mcp_vercel_uploadcert` - Upload a cert
- `mcp_vercel_removecert` - Remove cert

#### Secrets
- `mcp_vercel_getsecrets` - List secrets
- `mcp_vercel_createsecret` - Create a new secret
- `mcp_vercel_getsecret` - Get a single secret
- `mcp_vercel_renamesecret` - Change secret name
- `mcp_vercel_deletesecret` - Delete a secret

#### Authentication
- `mcp_vercel_listauthtokens` - List auth tokens
- `mcp_vercel_createauthtoken` - Create an auth token
- `mcp_vercel_getauthtoken` - Get auth token metadata
- `mcp_vercel_deleteauthtoken` - Delete an authentication token
- `mcp_vercel_getauthuser` - Get the authenticated user

#### Additional Features
- `mcp_vercel_requestpromote` - Points all production domains for a project to a given deploy
- `mcp_vercel_listpromotealiases` - Gets a list of aliases with status for the current promote
- `mcp_vercel_createcheck` - Create a new check
- `mcp_vercel_getallchecks` - Retrieve a list of all checks
- `mcp_vercel_getcheck` - Get a single check
- `mcp_vercel_updatecheck` - Update a check
- `mcp_vercel_rerequestcheck` - Rerun a check
- `mcp_vercel_uploadfile` - Upload deployment files
- `mcp_vercel_updateprojectprotectionbypass` - Update protection bypass for automation

---

## AWS Documentation MCP

**Status:** Enabled  
**Command:** uvx awslabs.aws-documentation-mcp-server@latest

### Functionality
The AWS Documentation MCP provides tools for searching and retrieving AWS documentation. It enables access to comprehensive AWS service documentation, guides, and API references.

### Available Tools

#### Documentation Search & Retrieval
- `mcp_aws_docs_search_documentation` - Search AWS documentation using the official AWS Documentation Search API
  - Supports filtering by product types and guide types
  - Returns search results with URLs, titles, and context snippets
  
- `mcp_aws_docs_read_documentation` - Fetch and convert an AWS documentation page to markdown format
  - Supports pagination for long documents
  - Converts HTML documentation to readable markdown
  
- `mcp_aws_docs_recommend` - Get content recommendations for an AWS documentation page
  - Returns highly rated, new, similar, and journey-based recommendations
  - Useful for discovering related documentation

---

## AWS API MCP

**Status:** Enabled  
**Command:** uvx awslabs.aws-api-mcp-server@latest  
**Auto-Approved Tools:** call_aws

### Functionality
The AWS API MCP provides tools for executing AWS CLI commands and managing AWS resources. It enables programmatic interaction with AWS services across compute, storage, databases, networking, and more.

### Available Tools

#### AWS CLI Execution
- `mcp_aws_api_call_aws` - Execute AWS CLI commands with validation and proper error handling
  - Supports all AWS services and operations
  - Includes pagination control
  - Validates commands before execution
  
- `mcp_aws_api_suggest_aws_commands` - Suggest AWS CLI commands based on natural language query
  - Provides up to 10 most likely AWS CLI commands
  - Includes confidence scores and required parameters
  - Useful when unsure about exact command syntax

---

## Netlify MCP

**Status:** Enabled  
**Command:** npx -y @netlify/mcp

### Functionality
The Netlify MCP provides tools for managing Netlify sites, deployments, and serverless functions. It enables site deployment, configuration management, and form handling.

### Available Tools

#### User & Team Management
- `mcp_netlify_netlify_user_services_reader` - Get user information
- `mcp_netlify_netlify_team_services_reader` - Get teams and team information

#### Project Management
- `mcp_netlify_netlify_project_services_reader` - Get project, projects, and forms for project
- `mcp_netlify_netlify_project_services_updater` - Update project settings, manage environment variables, create new projects

#### Deployment
- `mcp_netlify_netlify_deploy_services_reader` - Get deployment information
- `mcp_netlify_netlify_deploy_services_updater` - Deploy site

#### Extensions
- `mcp_netlify_netlify_extension_services_reader` - Get extensions and extension details
- `mcp_netlify_netlify_extension_services_updater` - Change extension installation, initialize database

#### Coding Rules
- `mcp_netlify_netlify_coding_rules` - Get coding rules for serverless functions, edge functions, blobs, image CDN, forms, and database

---

## AWS Diagram MCP

**Status:** Enabled  
**Command:** uvx awslabs.aws-diagram-mcp-server

### Functionality
The AWS Diagram MCP provides tools for generating architecture diagrams using the Python diagrams package. It enables creation of visual representations of AWS infrastructure and system architectures.

### Available Tools

#### Diagram Generation
- `mcp_awslabsaws_diagram_mcp_server_generate_diagram` - Generate a diagram from Python code using the diagrams package
  - Supports AWS, Kubernetes, on-premises, and custom diagrams
  - Returns path to generated PNG file
  
- `mcp_awslabsaws_diagram_mcp_server_get_diagram_examples` - Get example code for different types of diagrams
  - Provides templates for AWS, sequence, flow, class, K8s, on-premises, and custom diagrams
  
- `mcp_awslabsaws_diagram_mcp_server_list_icons` - List available icons from the diagrams package
  - Supports filtering by provider and service
  - Returns all available icons for creating diagrams

---

## Terraform MCP

**Status:** Enabled  
**Command:** uvx awslabs.terraform-mcp-server@latest

### Functionality
The Terraform MCP provides tools for Infrastructure as Code (IaC) development with Terraform. It enables Terraform configuration generation, validation, execution, security scanning, and AWS best practices guidance. This MCP is specifically designed for AWS infrastructure and includes Checkov integration for security compliance.

### Available Tools

#### Terraform Workflow Execution
- `mcp_awslabsterraform_mcp_server_ExecuteTerraformCommand` - Run Terraform commands directly
  - Supports: init, plan, validate, apply, destroy operations
  - Pass variables and specify AWS regions
  - Get formatted command output for analysis
  
- `mcp_awslabsterraform_mcp_server_ExecuteTerragruntCommand` - Run Terragrunt commands directly
  - Supports: init, plan, validate, apply, destroy, output, run-all operations
  - Configure terragrunt-config and include/exclude paths
  - Pass variables and specify AWS regions

#### Provider Documentation
- `mcp_awslabsterraform_mcp_server_SearchAwsProviderDocs` - Search AWS provider documentation for resources and attributes
  - Search for resources and data sources
  - Get descriptions, example code snippets, argument references, and attribute references
  - Supports both AWS and AWSCC providers
  
- `mcp_awslabsterraform_mcp_server_SearchAwsccProviderDocs` - Search AWSCC provider documentation
  - AWSCC provider based on AWS Cloud Control API
  - More consistent interface compared to standard AWS provider
  - Get schema information and example snippets

#### Module Analysis
- `mcp_awslabsterraform_mcp_server_SearchUserProvidedModule` - Search for and analyze Terraform Registry modules
  - Analyze input variables, output variables, and README content
  - Understand module usage and configuration options
  - Analyze module structure and dependencies
  
- `mcp_awslabsterraform_mcp_server_SearchSpecificAwsIaModules` - Search AWS-IA specialized modules for AI/ML workloads
  - Amazon Bedrock module for generative AI applications
  - OpenSearch Serverless for vector search capabilities
  - SageMaker endpoint deployment for ML model hosting
  - Serverless Streamlit application deployment for AI interfaces

#### Security & Compliance
- `mcp_awslabsterraform_mcp_server_RunCheckovScan` - Run Checkov security scan on Terraform code
  - Identify security and compliance issues
  - Get detailed remediation guidance
  - Automatically fix identified security issues when possible
  - Filter by specific check IDs or skip checks as needed

#### AWS Best Practices
The Terraform MCP provides guidance on:
- Terraform best practices for AWS
- AWS Well-Architected guidance for Terraform configurations
- Security and compliance recommendations
- AWSCC provider prioritization for consistent API behavior
- Security-first development workflow with validation and scanning

### Prerequisites
- `uv` - Python package manager (required)
- `terraform` CLI - For workflow execution (optional but recommended)
- `checkov` - For security scanning (optional)

### Key Features
✅ **Terraform Best Practices** - AWS-specific guidance for Infrastructure as Code  
✅ **Security Scanning** - Checkov integration for compliance and vulnerability detection  
✅ **AWS Provider Documentation** - Search AWS and AWSCC provider resources  
✅ **Terraform Workflow** - Execute init, plan, validate, apply, destroy commands  
✅ **Terragrunt Support** - Run Terragrunt commands for advanced IaC patterns  
✅ **Module Analysis** - Analyze Terraform Registry modules and AWS-IA modules  
✅ **Security-First Development** - Structured process for creating secure infrastructure code  

---

## AWS Terraform MCP

**Status:** Enabled  
**Command:** uvx awslabs.aws-terraform-mcp-server@latest

### Functionality
The AWS Terraform MCP provides specialized tools for AWS infrastructure management using Terraform. It combines AWS documentation, Terraform execution, security scanning, and best practices guidance into a unified interface for Infrastructure as Code development on AWS.

### Available Tools

#### Terraform Workflow Execution
- `mcp_awslabsterraform_mcp_server_ExecuteTerraformCommand` - Execute Terraform commands (init, plan, validate, apply, destroy)
  - Run Terraform operations in specified working directory
  - Pass variables and specify AWS regions
  - Get formatted output for analysis and debugging
  
- `mcp_awslabsterraform_mcp_server_ExecuteTerragruntCommand` - Execute Terragrunt commands (init, plan, validate, apply, destroy, output, run-all)
  - Run Terragrunt for advanced IaC patterns
  - Configure include/exclude directories for multi-module deployments
  - Support for custom terragrunt config files

#### AWS Provider Documentation
- `mcp_awslabsterraform_mcp_server_SearchAwsProviderDocs` - Search AWS Terraform provider documentation
  - Find resources and data sources
  - Get descriptions, examples, argument references, and attribute references
  - Supports both resources and data sources
  
- `mcp_awslabsterraform_mcp_server_SearchAwsccProviderDocs` - Search AWSCC provider documentation
  - AWSCC provider based on AWS Cloud Control API
  - More consistent interface compared to standard AWS provider
  - Get schema information and example code

#### Module Analysis & Discovery
- `mcp_awslabsterraform_mcp_server_SearchUserProvidedModule` - Analyze Terraform Registry modules
  - Understand input variables, outputs, and README content
  - Analyze module structure and dependencies
  - Get usage examples and configuration options
  
- `mcp_awslabsterraform_mcp_server_SearchSpecificAwsIaModules` - Search AWS-IA specialized modules
  - Amazon Bedrock module for generative AI applications
  - OpenSearch Serverless for vector search capabilities
  - SageMaker endpoint deployment for ML model hosting
  - Serverless Streamlit application deployment

#### Security & Compliance
- `mcp_awslabsterraform_mcp_server_RunCheckovScan` - Run Checkov security scan on Terraform code
  - Identify security and compliance issues
  - Get detailed remediation guidance
  - Filter by specific check IDs or skip checks
  - Automatically detect vulnerabilities and misconfigurations

### Prerequisites
- `uv` - Python package manager (required for running the MCP)
- `terraform` CLI - For workflow execution (optional but recommended)
- `checkov` - For security scanning (optional)

### Key Features
✅ **AWS-Specific Terraform Tools** - Specialized for AWS infrastructure management  
✅ **Security Scanning** - Checkov integration for compliance and vulnerability detection  
✅ **Provider Documentation** - Search AWS and AWSCC provider resources and data sources  
✅ **Terraform Execution** - Execute init, plan, validate, apply, destroy commands  
✅ **Terragrunt Support** - Run Terragrunt for advanced multi-module patterns  
✅ **Module Analysis** - Analyze Terraform Registry modules and AWS-IA modules  
✅ **Best Practices** - AWS Well-Architected guidance for Terraform configurations  
✅ **Security-First Development** - Structured process for creating secure infrastructure code  

### Use Cases
- **Infrastructure as Code Development** - Write and manage AWS infrastructure with Terraform
- **Security Compliance** - Scan Terraform code for security vulnerabilities and compliance issues
- **AWS Best Practices** - Follow AWS Well-Architected Framework recommendations
- **Multi-Module Deployments** - Use Terragrunt for complex infrastructure patterns
- **Module Discovery** - Find and analyze Terraform modules for AWS services
- **AI/ML Infrastructure** - Deploy Bedrock, SageMaker, and OpenSearch with AWS-IA modules

---

## Summary Table

| MCP | Status | Primary Use Case | Key Features |
|-----|--------|------------------|--------------|
| Supabase | Enabled | Backend & Database | PostgreSQL, Auth, Edge Functions, Branching |
| Playwright | Enabled | Browser Automation | Web Testing, Screenshots, Form Filling |
| GitHub | Enabled | Repository Management | Issues, PRs, Code Management |
| Vercel | Enabled | Deployment & Hosting | Projects, Deployments, Domains, Teams |
| AWS Documentation | Enabled | AWS Learning | Search, Read, Recommendations |
| AWS API | Enabled | AWS Resource Management | CLI Commands, All AWS Services |
| Netlify | Enabled | Site Deployment | Deployments, Functions, Forms |
| AWS Diagram | Enabled | Architecture Visualization | Diagram Generation, Icons |
| Terraform | Enabled | Infrastructure as Code | Terraform Execution, Security Scanning, AWS Best Practices |
| AWS Terraform | Enabled | AWS Infrastructure as Code | Terraform Execution, Checkov Scanning, AWS Provider Docs, Module Analysis |

---

## Getting Started

To use any of these MCPs:

1. Ensure the MCP is enabled in your `.kiro/settings/mcp.json` configuration
2. Use the tools directly in your Kiro chat or code
3. Refer to the specific tool documentation for parameters and usage
4. Some tools are auto-approved for faster execution (check your config)

For more information about configuring MCPs, visit the Kiro documentation or check the MCP configuration file.
