---
id: 6341
date: 2026-03-21T01:36:18+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
---

@drcha0s ROCm ставить НЕЛЬЗЯ.

  GECC got enabled by installing the AMD ROCm driver stack (boot -5 → boot -4   
  transition):                                                                  
                                                                                
  1. During boot -5 session (Mar 20, starting ~11:09), you ran:                 
  wget .../amdgpu-install_7.2.70200-1_all.deb                                   
  sudo apt install ./amdgpu-install_7.2.70200-1_all.deb                         
  amdgpu-install -y --usecase=graphics,rocm,opencl                            
  sudo reboot                                                                   
  2. The ROCm/amdgpu-install package enabled GECC as part of the RAS            
  (Reliability, Availability, Serviceability) feature set. This is default      
  behavior for ROCm workloads — it enables GPU ECC to protect against memory    
  bit-flips during compute tasks. The GECC flag is stored in the GPU            
  firmware/PSP, so it persists across reboots and takes effect on the next boot
  cycle.
  3. From boot -4 onward (Mar 20 22:38), GECC was active → VRAM dropped from
  32624M to 30576M (2048M ECC overhead).                                        
  4. You later uninstalled ROCm (sudo amdgpu-uninstall) and switched to
  Vulkan-based llama.cpp, but GECC stayed enabled in the GPU firmware —         
  uninstalling the driver doesn't reset it.
  5. You eventually noticed the VRAM loss and explicitly disabled it:           
  echo "options amdgpu ras_enable=0" | sudo tee /etc/modprobe.d/amdgpu.conf     
  sudo update-initramfs -u                                                      
  sudo reboot                                                                   
  5. This took effect on boot 0 (current), restoring full 32624M VRAM.          
                                                                                
  TL;DR: Installing amdgpu-install with ROCm usecase automatically enabled GECC 
  in the GPU firmware. It consumed 2 GB of VRAM for ECC parity. Uninstalling    
  ROCm didn't turn it off — you had to explicitly set amdgpu ras_enable=0 to    
  disable it.