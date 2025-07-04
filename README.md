# Remote Segment Anything (SAM) for CVAT

This repository provides a Nuclio function that integrates CVAT with a **remote Segment Anything Model (SAM)** server. Instead of running resource-intensive SAM locally, this implementation connects to a remote SAM instance, reducing local resource requirements while maintaining full functionality for semi-automated annotation.

## Key Features

- 🚀 **Reduced local resource usage** - SAM runs on remote hardware

- ⚡ **Seamless CVAT integration** - works like built-in SAM models

- 🔧 **Easy setup** - automated installation/configuration scripts

- 🌐 **Network flexible** - connect to local or cloud-based SAM servers


## Prerequisites

1. **CVAT Installation**: installed and running (follow [CVAT docs](https://docs.cvat.ai/docs))
    
2. **Nuclio CLI**: required for deployment (included in `install` script)
    
3. **Remote SAM Server**: running and accessible (e.g., [segment-anything-flask](https://github.com/ValV/sam-service))
    

## Directory Structure

```
cvat-nuclio-http/
├── valv/
│   └── sam/
│       └── nuclio/
│           ├── function.yaml    # Nuclio configuration
│           └── main.py          # SAM handler implementation
├── setup                        # deployment script
├── install                      # nuclio CLI installer
└── README.md                    # this documentation

```

## Installation

### Step 1: Clone Repository into CVAT

```bash
cd /path/to/cvat/serverless
git clone https://github.com/ValV/cvat-nuclio-http.git
cd cvat-nuclio-http
```

### Step 2: Install Nuclio CLI (if not available)

> Nuclio build subsystem requires `docker-buildx-plugin` to be installed. If it is not already installed, the installation script will try to do it.

```bash
chmod +x install
./install
```

### Step 3: Set up and Deploy Function

> Deploying a new function on build stage may require `python-is-python3` package installed.

```bash
# Set SAM_URI (replace with a valid custom endpoint)
export SAM_URI="http://example-sam-host:51515/features"

# Set up endpoint for the function
chmod +x setup
./setup

# Deploy to CVAT
cd /path/to/cvat/serverless
./deploy_cpu.sh
```

Alternative deployment without environment variables:

```bash
# Set up endpoint for the function
./setup "http://example-sam-host:51515/features"

# Deploy to CVAT
cd /path/to/cvat/serverless
./deploy_cpu.sh
```

## Configuration

### SAM_URI Formats

- Local network: `http://192.168.1.100:51515/features`
    
- Cloud instance: `https://sam.example.com/features`
    
- Docker network: `http://sam-container:51515/features`
    

### Advanced Options

Edit `function.yaml` to customize:

```yaml
spec:
  minReplicas: 2          # Increase for high load
  maxReplicas: 5
  eventTimeout: 60s        # Increase for large images
  triggers:
    http:
      maxWorkers: 4        # Concurrent request handlers
```

## Verification

1. **Check Nuclio dashboard** at `http://localhost:8070` (default)
    
2. **Verify function status**:
    
```bash
nuctl get functions
```
    
3. **Test functionality** in CVAT:
    
    - Open annotation interface
        
    - Select "Segment Anything X" model
        
    - Add positive/negative points on an object
        

## Usage in CVAT

1. Create/Open a project in CVAT
    
2. Open annotation view
    
3. Select "Segment Anything X" from models
    
4. Place points on objects:
    
    - ✅ **Positive points**: Object interior
        
    - ❌ **Negative points**: Exclude areas
        
5. Press `Submit` to create mask
    
![hrnet_example.gif](https://raw.githubusercontent.com/opencv/cvat/develop/site/content/en/images/hrnet_example.gif)

## Network Architecture

```
┌─────────┐   HTTPS   ┌────────┐   ┌──────────────┐   HTTP    ┌────────────┐
│  CVAT   │──────────>│  CVAT  │──>│    Nuclio    │──────────>│   Remote   │
│ Browser │<──────────│ Server │<──│ SAM Function │<──────────│ SAM Server │
└─────────┘  (Embed)  └────────┘   └──────────────┘  (Embed)  └────────────┘
```

## Troubleshooting

### Common Issues

**Function not appearing in CVAT:**

- Verify deployment namespace matches CVAT (`cvat` by default)
    
- Check for errors in Nuclio dashboard
    

**Connection timeouts:**

- Verify network connectivity to SAM server
    
- Check firewall rules on remote host
    
- Test with curl: `curl http://example-sam-host:51515/health`
    

**Mask quality issues:**

- Ensure remote SAM uses same weights as local version
    
- Increase `eventTimeout` for high-resolution images
    

## Maintenance

### Update SAM URI

```bash
# Redeploy with new URI
git reset --hard HEAD
./setup "http://new-sam-uri:51515/features"
```

### Uninstall

```bash
nuctl delete function pth-facebookresearch-sam-vit-h
```

## Contributing

Pull requests welcome! Please follow:

1. Maintain compatibility with CVAT's serverless interface
    
2. Keep configuration templates generic
    
3. Document new features thoroughly
    

## License

MIT License - See [LICENSE](./LICENSE) file.

---

This implementation provides a resource-efficient way to leverage powerful SAM models in CVAT while maintaining the flexibility to run SAM on specialized hardware. For optimal performance, ensure low-latency network connection between CVAT instance and SAM server.