#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.3.3 - Ensure default user umask is configured
# Source Page: 720
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following to verify the default user umask is set to 027(octal) or u=rwx,g=rx,o=
# (Symbolic) to enforce newly created directories' permissions to be 750 (drwxr-x---),
# and newly created file's permissions be 640 (rw-r-----), or more restrictive:
# #!/usr/bin/env bash
# {
# l_output="" l_output2=""
# file_umask_chk()
# {
# if grep -Psiq -- '^\h*umask\h+(0?[0-7][2-
# 7]7|u(=[rwx]{0,3}),g=([rx]{0,2}),o=)(\h*#.*)?$' "$l_file"; then
# l_output="$l_output\n - umask is set correctly in \"$l_file\""
# elif grep -Psiq -- '^\h*umask\h+(([0-7][0-7][01][0-7]\b|[0-7][0-7][0-
# 7][0-6]\b)|([0-7][01][0-7]\b|[0-7][0-7][0-
# 6]\b)|(u=[rwx]{1,3},)?(((g=[rx]?[rx]?w[rx]?[rx]?\b)(,o=[rwx]{1,3})?)|((g=[wrx
# ]{1,3},)?o=[wrx]{1,3}\b)))' "$l_file"; then
# l_output2="$l_output2\n - umask is incorrectly set in \"$l_file\""
# fi
# }
# while IFS= read -r -d $'\0' l_file; do
# file_umask_chk
# done < <(find /etc/profile.d/ -type f -name '*.sh' -print0)
# [ -z "$l_output" ] && l_file="/etc/profile" && file_umask_chk
# [ -z "$l_output" ] && l_file="/etc/bashrc" && file_umask_chk
# [ -z "$l_output" ] && l_file="/etc/bash.bashrc" && file_umask_chk
# [ -z "$l_output" ] && l_file="/etc/pam.d/postlogin"
# if [ -z "$l_output" ]; then
# if grep -Psiq --
# '^\h*session\h+[^#\n\r]+\h+pam_umask\.so\h+([^#\n\r]+\h+)?umask=(0?[0-7][2-
# 7]7)\b' "$l_file"; then
# l_output1="$l_output1\n - umask is set correctly in \"$l_file\""
# elif grep -Psiq
# '^\h*session\h+[^#\n\r]+\h+pam_umask\.so\h+([^#\n\r]+\h+)?umask=(([0-7][0-
# 7][01][0-7]\b|[0-7][0-7][0-7][0-6]\b)|([0-7][01][0

# Remediation candidate
done < <(find /etc/profile.d/ -type f -name '*.sh' -print0)
l_file="/etc/profile" && file_umask_chk
l_file="/etc/bashrc" && file_umask_chk
l_file="/etc/bash.bashrc" && file_umask_chk
l_file="/etc/pam.d/postlogin"
l_file="/etc/login.defs" && file_umask_chk
l_file="/etc/default/login" && file_umask_chk
echo -e " - Configure UMASK in a file in the \"/etc/profile.d/\"
/etc/profile.d/50-systemwide_umask.sh\n"

# TODO: replace the commented/manual steps above with validated bash remediation logic.
