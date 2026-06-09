import os
import gc
import psutil


def execute_system_ram_cleanup() -> float:
    """
    Forces garbage collection within LapPulse and purges the working sets
    of accessible processes on Windows to free up system-wide memory.
    
    Returns:
        float: Reclaimed system memory in Megabytes (MB).
    """
    before_mem = psutil.virtual_memory().available

    gc.collect()

    if os.name == 'nt':
        try:
            import ctypes
            
            # Flush the working set of the current process (LapPulse itself)
            ctypes.windll.psapi.EmptyWorkingSet(-1)
            
            # Iterate through all active system processes to perform a system-wide memory flush
            # Note: This block requires the application to be executed with Administrator privileges
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Access flag specifying full control permissions to open the target process
                    PROCESS_ALL_ACCESS = 0x1F0FFF
                    
                    # Obtain a secure handle to the target process using its Process ID (PID)
                    h_process = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, proc.info['pid'])
                    
                    if h_process:
                        # Purge the working set of the opened process to reclaim physical memory
                        ctypes.windll.psapi.EmptyWorkingSet(h_process)
                        
                        # Safely close the process handle to prevent resource/memory leaks
                        ctypes.windll.kernel32.CloseHandle(h_process)
                        
                except Exception:
                    # Gracefully skip processes where access is denied or protected by the OS
                    continue
                    
        except Exception as win_err:
            print(f"Windows memory optimization subsystem warning: {win_err}")

    after_mem = psutil.virtual_memory().available
    bytes_freed = max(0, after_mem-before_mem)
    return bytes_freed/(1024*1024)
