if not sysconf.getReadOnly():
    if not sysconf.has("rpm-strict-multilib"):
        sysconf.set("rpm-strict-multilib", True, weak=True)
    if not sysconf.has("sync-urpmi-medialist"):
        sysconf.set("sync-urpmi-medialist", True, weak=True)

