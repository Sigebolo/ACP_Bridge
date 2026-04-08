# GPT-SoVITS TTS Deployment Handoff Report

## 1. Project Overview
The goal was to deploy a state-of-the-art emotional Text-to-Speech (TTS) system using GPT-SoVITS on GCP, integrated with OpenClaw via a compatibility bridge.

## 2. Infrastructure Details
- **Server Name**: `heartbeat-bot-server2` (GCP)
- **Zone**: `us-central1-a`
- **Machine Type**: `g2-standard-4` (4 vCPUs, 16GB RAM)
- **GPU**: NVIDIA L4 (24GB VRAM)
- **OS**: Debian 11 (Bullseye) / Python 3.10 (Conda base)
- **Public IP**: `34.42.163.233`
- **Internal Ports**:
  - `9880`: GPT-SoVITS API (Default)
  - `5000`: OpenClaw Bridge (Inbound from bots)

## 3. Installation Paths
- **Base Directory**: `/home/Administrator/GPT-SoVITS`
- **Reference Audio**: `/home/Administrator/GPT-SoVITS/ref_audio/`
  - Target Voice: `heartbeat_v14_voice.mp3`
- **Bridge Script**: `/home/Administrator/GPT-SoVITS/sovits_bridge.py`
- **Deployment Script**: `/home/Administrator/deploy_tts.sh`

## 4. Key Dependencies Resolved
The following modules were missing from the base image and have been installed in `/opt/conda`:
- `fastapi`, `uvicorn`, `httpx` (Bridge)
- `ffmpeg`, `ffmpeg-python`, `PySoundFile` (Audio backend)
- `jieba`, `jieba_fast`, `pypinyin`, `langid` (NLP frontend)
- `x-transformers`, `einops>=0.8.0`, `onnxruntime-gpu` (Engine core)

## 5. Current Issues & Troubleshooting
### Persistent `ModuleNotFoundError: jieba`
Despite multiple installations, the background process (launched via `nohup`) sometimes fails to recognize `jieba`.
- **Root Cause**: Likely a `PYTHONPATH` or `sys.path` priority conflict where the engine ignores standard site-packages.
- **Current Workaround**: `jieba` and related modules have been brute-forced (installed with `-t .`) into the project root and subdirectories to ensure discovery.
- **Recommended Action**: Use the consolidated `deploy_tts.sh` to launch, ensuring explicit `export PYTHONPATH=/home/Administrator/GPT-SoVITS` is set.

## 6. Integration Checklist
- [x] GPT-SoVITS Engine source code installed.
- [x] High-fidelity voice sample uploaded.
- [x] Bridge proxy (`sovits_bridge.py`) written.
- [ ] Final end-to-end verification of `POST /tts` output.

## 7. Launch Command (Reference)
To start everything safely:
```bash
bash /home/Administrator/deploy_tts.sh
```
Or manually:
```bash
cd /home/Administrator/GPT-SoVITS
export PYTHONPATH=/home/Administrator/GPT-SoVITS
nohup /opt/conda/bin/python api_v2.py > ~/sovits_api.log 2>&1 &
# Wait 30s
nohup /opt/conda/bin/python sovits_bridge.py > ~/bridge.log 2>&1 &
```

## 8. Handoff Contact
Antigravity AI (Task ID: `716c770d-8592-415e-a566-fa48dff8c1d0`).
