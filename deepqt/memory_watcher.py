import psutil
from PySide6.QtCore import Signal, QObject, QTimer

# Attempt to import pynvml for GPU monitoring
try:
    import pynvml

    _pynvml_available = True
except ImportError:
    _pynvml_available = False


class MemoryWatcher(QObject):
    # Monitor system memory usage to warn of impending OOM errors.
    oom_warning = Signal(str)
    oom_relaxed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_memory)
        self.gpu_available = False

        if _pynvml_available:
            try:
                pynvml.nvmlInit()
                device_count = pynvml.nvmlDeviceGetCount()
                if device_count > 0:
                    self.gpu_available = True
            except pynvml.NVMLError:
                self.gpu_available = False
        else:
            self.gpu_available = False

    def start(self):
        # Start the timer to check memory every second (2000 ms)
        self.timer.start(2000)

    def stop(self):
        # Stop the timer
        self.timer.stop()

    def check_memory(self):
        # Monitor system memory (RAM)
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        oom: bool = False

        # Check conditions for RAM and swap.
        if swap.total == 0:  # No swap available.
            if mem.percent >= 80:
                self.oom_warning.emit(
                    self.tr("RAM usage has reached {mem}%").format(mem=round(mem.percent))
                )
                oom = True
        else:  # Swap is available
            if mem.percent >= 90:
                self.oom_warning.emit(
                    self.tr("RAM usage has reached {mem}%").format(mem=round(mem.percent))
                )
                oom = True

        # Monitor VRAM if GPUs are available
        if self.gpu_available:
            try:
                device_count = pynvml.nvmlDeviceGetCount()
                for i in range(device_count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    vram_total = meminfo.total
                    vram_used = meminfo.used
                    vram_percent = (vram_used / vram_total) * 100
                    if vram_percent >= 80:
                        self.oom_warning.emit(
                            "GPU {gpu}: VRAM usage has reached {vmem}%".format(
                                gpu=i, vmem=round(vram_percent)
                            )
                        )
                        oom = True
            except pynvml.NVMLError as err:
                # Handle NVML errors
                print(f"Error querying GPU memory: {err}")

        if not oom:
            self.oom_relaxed.emit()

    def __del__(self):
        if self.gpu_available and _pynvml_available:
            try:
                pynvml.nvmlShutdown()
            except pynvml.NVMLError:
                pass
