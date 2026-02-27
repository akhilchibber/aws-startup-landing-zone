"""
GitHub Issue creator for Account Factory integration.
"""
import boto3
import time
from github import Github, GithubException
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError


class GitHubIssueCreator:
    """Creates GitHub Issues for Account Factory workflow."""

    def __init__(self, secret_arn: str, repo_name: str):
        """Initialize GitHub client with Secrets Manager integration."""
        self.secret_arn = secret_arn
        self.repo_name = repo_name
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def get_github_client(self) -> Github:
        """Get GitHub client with token from Secrets Manager."""
        secrets_client = boto3.client('secretsmanager')
        
        try:
            response = secrets_client.get_secret_value(SecretId=self.secret_arn)
            token = response['SecretString']
            return Github(token)
        except ClientError as e:
            raise Exception(f"Failed to retrieve GitHub token: {e}")

    def format_issue_body(self, answers: Dict[str, Any]) -> str:
        """Format issue body to match Account Factory template exactly."""
        # Extract answers with defaults for optional fields
        team_name = answers.get('team_name', '')
        team_lead = answers.get('team_lead', '')
        email = answers.get('email', '')
        cost_center = answers.get('cost_center', '')
        data_classification = answers.get('data_classification', '')
        business_criticality = answers.get('business_criticality', '')
        use_case = answers.get('use_case', '')
        budget = answers.get('budget', '')
        aws_services = answers.get('aws_services', '')
        compliance = answers.get('compliance', 'none')

        # Format exactly as the GitHub Issue template expects
        body = f"""### Team Information

**Team Name:** {team_name}
**Team Lead:** {team_lead}
**Email:** {email}
**Cost Center:** {cost_center}

### Account Requirements

**Data Classification:** {data_classification}
**Business Criticality:** {business_criticality}
**Primary Use Case:** {use_case}
**Monthly Budget (USD):** ${budget}

### Technical Details

**AWS Services:** {aws_services if aws_services else 'Not specified'}
**Compliance Requirements:** {compliance}

---
*This issue was created via Bedrock Conversational Intake*
"""
        return body

    def create_issue(self, answers: Dict[str, Any]) -> Optional[int]:
        """Create GitHub Issue with retry logic."""
        team_name = answers.get('team_name', 'unknown-team')
        title = f"New AWS Account Request: {team_name}"
        body = self.format_issue_body(answers)
        labels = ['account-request', 'automated']

        for attempt in range(self.max_retries):
            try:
                github = self.get_github_client()
                repo = github.get_repo(self.repo_name)
                
                issue = repo.create_issue(
                    title=title,
                    body=body,
                    labels=labels
                )
                
                return issue.number
            
            except GithubException as e:
                if e.status == 401:
                    raise Exception("GitHub authentication failed. Check token permissions.")
                elif e.status == 403:
                    if 'rate limit' in str(e).lower():
                        if attempt < self.max_retries - 1:
                            time.sleep(self.retry_delay * (attempt + 1))
                            continue
                        raise Exception("GitHub rate limit exceeded")
                    raise Exception("GitHub authorization failed. Check repository access.")
                elif e.status == 404:
                    raise Exception(f"Repository not found: {self.repo_name}")
                else:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue
                    raise Exception(f"GitHub API error: {e}")
            
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise Exception(f"Failed to create GitHub Issue: {e}")
        
        return None
