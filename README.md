# Fusion Odoo Modules - CI/CD Pipeline

This repository contains custom Odoo modules with an automated CI/CD pipeline for seamless deployment.

## 🚀 CI/CD Pipeline Features

- **Automatic Validation**: Python syntax checking and module validation
- **Auto-merge**: Staging branch automatically merges to main on successful push
- **Smart Deployment**: Automatically detects changes and restarts services as needed
- **Container Management**: Handles Odoo and reverse proxy container restarts
- **Deployment Tagging**: Creates deployment tags for tracking

## 📋 Repository Structure

```
/root/addons/Fusion/
├── .github/workflows/deploy.yml    # GitHub Actions CI/CD pipeline
├── deploy.sh                       # Production deployment script
├── .pre-commit-config.yaml        # Code quality hooks
├── auto_database_backup/           # Database backup module
├── login_bg_minimal/              # Login background module
├── muk_web_*/                     # MuK web modules
└── README.md                      # This file
```

## 🔧 Setup Instructions

### 1. GitHub Repository Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
PROD_HOST=your_server_ip
PROD_USER=root
PROD_SSH_KEY=your_private_ssh_key
PROD_PORT=22
GITHUB_TOKEN=your_github_token (usually auto-provided)
```

### 2. SSH Key Setup

Generate SSH key pair for GitHub Actions:
```bash
ssh-keygen -t rsa -b 4096 -C "github-actions@yourdomain.com"
```

Add the public key to your server's `~/.ssh/authorized_keys` and the private key to GitHub secrets.

### 3. Server Configuration

Ensure your production server has:
- Git installed and configured
- Docker and Docker Compose (if using containers)
- Proper permissions for the deployment user

## 🔄 Workflow Process

1. **Developer pushes to staging branch**
2. **GitHub Actions triggers**:
   - Validates Python syntax
   - Checks module structure
   - Runs pre-commit hooks
3. **If validation passes**:
   - Merges staging to main
   - Deploys to production server
   - Runs deployment script
   - Restarts services if needed
   - Creates deployment tag

## 🛠 Manual Deployment

To deploy manually:
```bash
cd /root/addons/Fusion
./deploy.sh
```

## 📦 Container Management

The pipeline automatically handles:
- **Odoo Container**: Restarts when Python/XML/CSV files change
- **Reverse Proxy**: Restarts when configuration files change
- **Cache Clearing**: Handles static file updates

## 🔍 Monitoring

Check deployment status:
- GitHub Actions tab in your repository
- Server logs: `journalctl -u docker` or container logs
- Odoo logs: `docker logs odoo_container_name`

## 🚨 Troubleshooting

### Common Issues:

1. **SSH Connection Failed**
   - Verify SSH key is correct
   - Check server IP and port
   - Ensure firewall allows connections

2. **Git Permission Denied**
   - Check SSH key has repository access
   - Verify Git configuration on server

3. **Container Restart Failed**
   - Check Docker service status
   - Verify container names in deploy.sh
   - Check Docker Compose configuration

### Debug Commands:
```bash
# Check container status
docker ps -a

# View container logs
docker logs container_name

# Test SSH connection
ssh -i ~/.ssh/key user@server

# Check Git status
git status && git remote -v
```

## 📝 Development Workflow

1. Create feature branch from staging:
   ```bash
   git checkout staging
   git pull origin staging
   git checkout -b feature/your-feature
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

3. Push to staging:
   ```bash
   git checkout staging
   git merge feature/your-feature
   git push origin staging
   ```

4. **Automatic deployment triggers!** 🚀

## 🔒 Security Notes

- SSH keys should be kept secure
- Use strong passwords for server access
- Regularly rotate SSH keys
- Monitor deployment logs for suspicious activity
- Keep Odoo and system packages updated

## 📞 Support

For issues with the CI/CD pipeline:
1. Check GitHub Actions logs
2. Review server deployment logs
3. Verify all secrets are correctly configured
4. Test SSH connectivity manually
