provider "github" {
  owner = "KothaGPT"
  token  = var.github_token
}

resource "github_organization_settings" "defaults" {
  secret_scanning_enabled = true
  dependency_graph_enabled = true
}

# Create teams
resource "github_team" "maintainers" {
  name        = "maintainers"
  description = "Core maintainers for KothaGPT projects"
}
Notes: use the HashiCorp GitHub provider; manage secrets & state carefully. See Terraform docs for up-to-date resources.