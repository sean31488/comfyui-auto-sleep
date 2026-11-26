# ComfyUI Auto Sleep

Hibernates the PC after the ComfyUI queue finishes.

<!-- screenshot: off / on / countdown -->

## Usage

Click the sleep button in the top menu to turn it on. Once queued work finishes, a 60-second countdown starts, then the PC hibernates.

- Click again to turn it off or cancel the countdown.
- Queuing a new task cancels the countdown.
- Resets to off when ComfyUI restarts.

## Requirements

- Windows only. On other platforms the extension stays disabled.
- Hibernation enabled: `powercfg /hibernate on`

## Install

```
cd ComfyUI/custom_nodes
git clone https://github.com/sean31488/comfyui-auto-sleep
```

## License

MIT. Provided as-is, maintained on a best-effort basis.
