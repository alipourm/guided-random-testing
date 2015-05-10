Z = 1.96
FEATURES_MIN = 0
FEATURES_MAX = 42
SUPRESSOR = 'S'
IRRELAVENT = 'I'
TRIGGER = 'T'
COVSUMMARYFILE = "covsummary.npy"


features = ["startup",
            "mount",
            "mount2",
            "unmount",
            "unmount2",
            "remount",
            "open",
            "close",
            "mkdir",
            "rmdir",
            "lseek",
            "truncate",
            "ftruncate",
            "stat",
            "fstat",
            "lstat",
            "read",
            "write",
            "freespace",
            "opendir",
            "readdir",
            "rewinddir",
            "closedir",
            "link",
            "symlink",
            "readlink",
            "unlink",
            "rename",
            "chmod",
            "fchmod",
            "fsync",
            "fdatasync",
            "access",
            "dup",
            "pread",
            "pwrite",
            "utime",
            "futime",
            "flush",
            "sync",
             "totalspace",
            "inodecount",
            "nhandles"]
