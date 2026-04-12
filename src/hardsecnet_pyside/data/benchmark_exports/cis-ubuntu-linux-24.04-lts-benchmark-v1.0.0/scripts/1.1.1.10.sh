#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.1.10 - Ensure unused filesystems kernel modules are not available
# Source Page: 69
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to:
# -
# Look at the filesystem kernel modules available to the currently running kernel.
# -
# Exclude mounted filesystem kernel modules that don't currently have a CVE
# -
# List filesystem kernel modules that are not fully disabled, or are loaded into the
# kernel
# Review the generated output
# Page 70
# #! /usr/bin/env bash
# {
# a_output=(); a_output2=(); a_modprope_config=(); a_excluded=(); a_available_modules=()
# a_ignore=("xfs" "vfat" "ext2" "ext3" "ext4")
# a_cve_exists=("afs" "ceph" "cifs" "exfat" "ext" "fat" "fscache" "fuse" "gfs2" "nfs_common"
# "nfsd" "smbfs_common")
# f_module_chk()
# {
# l_out2=""; grep -Pq -- "\b$l_mod_name\b" <<< "${a_cve_exists[*]}" && l_out2=" <- CVE
# exists!"
# if ! grep -Pq -- '\bblacklist\h+'"$l_mod_name"'\b' <<< "${a_modprope_config[*]}"; then
# a_output2+=(" - Kernel module: \"$l_mod_name\" is not fully disabled $l_out2")
# elif ! grep -Pq -- '\binstall\h+'"$l_mod_name"'\h+(\/usr)?\/bin\/(false|true)\b' <<<
# "${a_modprope_config[*]}"; then
# a_output2+=(" - Kernel module: \"$l_mod_name\" is not fully disabled $l_out2")
# fi
# if lsmod | grep "$l_mod_name" &> /dev/null; then # Check if the module is currently loaded
# l_output2+=(" - Kernel module: \"$l_mod_name\" is loaded" "")
# fi
# }
# while IFS= read -r -d $'\0' l_module_dir; do
# a_available_modules+=("$(basename "$l_module_dir")")
# done < <(find "$(readlink -f /lib/modules/"$(uname -r)"/kernel/fs)" -mindepth 1 -maxdepth 1 -
# type d ! -empty -print0)
# while IFS= read -r l_exclude; do
# if grep -Pq -- "\b$l_exclude\b"

# Remediation candidate
# IF - the module is available in the running kernel:
in the /etc/modprobe.d/ directory
/etc/modprobe.d/ directory
# modprobe -r gfs2 2>/dev/null
/etc/modprobe.d/gfs2.conf
a_showconfig=() # Create array with modprobe output
done < <(modprobe --showconfig | grep -P --
modprobe -r "$l_mod_name" 2>/dev/null; rmmod "$l_mod_name"
/etc/modprobe.d/"$l_mod_name".conf
/etc/modprobe.d/"$l_mod_name".conf

# TODO: replace the commented/manual steps above with validated bash remediation logic.
